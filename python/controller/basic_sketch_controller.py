# coding=utf-8

import os
import sys
import socket
import logging
from model.flow_definitions import *

if sys.version > '3':  ## if using python3
    sys.path.append(os.environ['HOME'] + "/P4/basic_p4_measurement/utils/p4utils_to_python3")
    #    sys.path.append("../../utils/p4utils-to-python3")
    from topology import Topology
    from sswitch_API import *
    import queue as Queue
else:  ## if using python2
    import Queue
    from p4utils.utils.topology import Topology
    from p4utils.utils.sswitch_API import *

from hash_functions import CrcCustom
from hash_functions import HashEx32
from hash_functions import calc_combined_hash_salt32

crc32_polinomials = [0x04C11DB7, 0xEDB88320, 0xDB710641, 0x82608EDB, 0x0192A90C,
                     0x741B8CD7, 0xEB31D82E, 0xD663B054, 0xBA0DC66B, 0x23894320,
                     0x32583499, 0x992C1A4C, 0x91129191, 0xAC593820, 0xBED19201,
                     0xFCA92083, 0x3911AECB, 0x10125723, 0xCE123B7A, 0xFEC928CA,
                     ]
"""crc32_polinomials (list): crc32_custom伪随机哈希函数要使用的种子列表。
这个数组的长度必须和p4src/hash_function_run_crc32_custom.p4文件中调用HashAlgorithm.crc32_custom的次数保持一致。
"""

import random

random.seed(0x11112222)


class BasicSketchController(SimpleSwitchAPI):
    """软件交换机的局部控制面Local Controller的基类，专用于流量测量Sketch。

    在BMv2软件交换机中部署各种流量测量Sketches的时候，需要在控制面设计对应的Queriers，实现离线查询功能．
    Controller类将为各种Queriers提供公共服务功能，包括用和BMv2交换机建立一对一thrift连接，初始化该交换机的哈希函数, 解析该交换机对应的流记录ground_truth文件.

    Controller的参考设计来自：https://github.com/uni-tue-kn/p4-macsec/blob/master/controller_distributed/switch_controller.py
    TODO(csqjxiao): 未来考虑实现多种交换机类型：type="bmv2"、"tofino"、"netfpga"、"alveo_u25"

    构造函数

    Args:
        sw_name (str): 控制器要关联的mininet虚拟交换机的名称
    """

    _instances = set()  # all instances of this BasicSketchController

    ENABLE_CRC32_CUSTOM = False
    hash_master_seed = 0x22221111  # for xxhash function

    def __init__(self, sw_name, sw_ip='localhost', sw_type='bmv2'):
        BasicSketchController._instances.add(self)

        if sw_type == 'bmv2':
            self.topology = Topology(db="topology.db")
            self.sw_name = sw_name
            self.thrift_port = self.topology.get_thrift_port(sw_name)
            self.thrift_ip = sw_ip
            super(BasicSketchController, self).__init__(self.thrift_port, self.thrift_ip)
        elif sw_type == 'tofino':
            raise Error
        elif sw_type == 'netfpga':
            raise Error

        if len(BasicSketchController._instances) == 1:
            BasicSketchController.create_hashes()  # the same set of hash funs for all BasicSketchController objects

        if BasicSketchController.ENABLE_CRC32_CUSTOM:
            self.custom_calcs = super(BasicSketchController, self).get_custom_crc_calcs()
            self.set_crc32_custom_hash_seeds()  # set hash seeds for the corresponding switch
        else:
            self.set_hash_master_seed()

    def __del__(self):
        BasicSketchController._instances.remove(self)

        # 查看 p4utils_to_python3/runtime_API.py 文件，755-761行代码实现了thrift connection.
        # We need to close the TCP connection underlying the two thrift client to avoid socket resource waste.

        # standard_client, mc_client = thrift_connect(
        #     thrift_ip, thrift_port,
        #     RuntimeAPI.get_thrift_services(pre_type)
        # )
        # load_json_config(standard_client, json_path)#youwenti
        # self.client = standard_client
        # self.mc_client = mc_client

        # self.client.close()
        # self.mc_client.close()

    @classmethod
    def all_controllers_reset_hash_seeds(cls):
        if BasicSketchController.ENABLE_CRC32_CUSTOM:
            for i in range(0, len(crc32_polinomials)):
                crc32_polinomials[i] = random.randint(0, 0xFFFFFFFF)
        else:
            BasicSketchController.hash_master_seed = random.randint(0, 0xFFFFFFFF)

        # create the same set of hash functions for all BasicSketchController objects
        cls.create_hashes()

        for controller in cls._instances:
            if BasicSketchController.ENABLE_CRC32_CUSTOM:
                controller.custom_calcs = super(BasicSketchController, controller).get_custom_crc_calcs()
                # set hash seeds for the corresponding switch
                controller.set_crc32_custom_hash_seeds()
            else:
                controller.set_hash_master_seed()

    def set_hash_master_seed(self):
        seed_str = "hash_master_seed"
        super(BasicSketchController, self).register_write(seed_str, 0, BasicSketchController.hash_master_seed)
        seeds = super(BasicSketchController, self).register_read(seed_str)
        if len(seeds) != 1 or seeds[0] != BasicSketchController.hash_master_seed:
            raise ValueError
        # print("switch '%s': configure master seed = 0x%x" % (self.sw_name, seeds[0]))

    def set_crc32_custom_hash_seeds(self):
        """为数据面，设置伪随机哈希函数．缺省使用crc32函数，并使用crc32_polinomials数组中定义的随机数种子。

        Args:
            None

        Returns:
            None
        """
        i = 0
        for custom_crc32, width in self.custom_calcs.items():
            if i < len(crc32_polinomials):
                super(BasicSketchController, self).set_crc32_parameters(custom_crc32, crc32_polinomials[i],
                                                                        0xFFFFFFFF, 0xFFFFFFFF, True, True)
                i += 1
            else:
                super(BasicSketchController, self).set_crc32_parameters(custom_crc32, crc32_polinomials[17],
                                                                        0xFFFFFFFF, 0xFFFFFFFF, True, True)

    @classmethod
    def create_hashes(cls):
        """初始化控制面的伪随机哈希函数，使得控制面和数据面的哈希函数完全一致．在构造函数中，缺省会调用这个方法．

        Args:
            sketch_number (int):　交换机上要运行的sketches的数目，为它们创建对应的Hash函数．比如，countmin sketches需要四行register array，则该参数为4．

        Returns:
            None: 无返回值，创建的哈希函数直接放在cls.hashes_xxxx列表中，包括hashes_1tuple_srcIP、hashes_1tuple_dstIP、hashes_2tuple、hashes_5tuple四个列表。

        """
        cls.num_of_hashes_1tuple_srcIP = 5
        cls.num_of_hashes_1tuple_dstIP = 5
        cls.num_of_hashes_2tuple = 5
        cls.num_of_hashes_5tuple = 5

        index_of_hashes = [0]
        index_of_hashes.append(index_of_hashes[0] + cls.num_of_hashes_1tuple_srcIP)
        index_of_hashes.append(index_of_hashes[1] + cls.num_of_hashes_1tuple_dstIP)
        index_of_hashes.append(index_of_hashes[2] + cls.num_of_hashes_2tuple)
        index_of_hashes.append(index_of_hashes[3] + cls.num_of_hashes_5tuple)

        hash_function_number = len(crc32_polinomials)
        if hash_function_number != index_of_hashes[4]:
            raise ValueError

        cls.hashes_1tuple_srcIP = []
        cls.hashes_1tuple_dstIP = []
        cls.hashes_2tuple = []
        cls.hashes_5tuple = []

        for i in range(hash_function_number):
            if BasicSketchController.ENABLE_CRC32_CUSTOM:
                hash_fun = CrcCustom(32, crc32_polinomials[i], True, 0xFFFFFFFF, True, 0xFFFFFFFF)

            if index_of_hashes[0] <= i < index_of_hashes[1]:
                if not BasicSketchController.ENABLE_CRC32_CUSTOM:
                    hash_fun = HashEx32(salt=calc_combined_hash_salt32(cls.hash_master_seed, i - index_of_hashes[0]))
                cls.hashes_1tuple_srcIP.append(hash_fun)
            elif index_of_hashes[1] <= i < index_of_hashes[2]:
                if not BasicSketchController.ENABLE_CRC32_CUSTOM:
                    hash_fun = HashEx32(salt=calc_combined_hash_salt32(cls.hash_master_seed, i - index_of_hashes[1]))
                cls.hashes_1tuple_dstIP.append(hash_fun)
            elif index_of_hashes[2] <= i < index_of_hashes[3]:
                if not BasicSketchController.ENABLE_CRC32_CUSTOM:
                    hash_fun = HashEx32(salt=calc_combined_hash_salt32(cls.hash_master_seed, i - index_of_hashes[2]))
                cls.hashes_2tuple.append(hash_fun)
            elif index_of_hashes[3] <= i < index_of_hashes[4]:
                if not BasicSketchController.ENABLE_CRC32_CUSTOM:
                    hash_fun = HashEx32(salt=calc_combined_hash_salt32(cls.hash_master_seed, i - index_of_hashes[3]))
                cls.hashes_5tuple.append(hash_fun)

        # print("len hashes_1tuple_srcIP: %d" % len(cls.hashes_1tuple_srcIP))
        # print("len hashes_1tuple_dstIP: %d" % len(cls.hashes_1tuple_dstIP))
        # print("len hashes_2tuple: %d" % len(cls.hashes_2tuple))
        # print("len hashes_5tuple: %d" % len(cls.hashes_5tuple))

    @classmethod
    def get_hash_function(cls, flow_rec, index):
        """返回flow_rec（一元组，二元组，五元组）适用的哈希函数，从适合的函数集中返回index指定的哈希函数.

        Args:
            flow_rec (flow_record): 流记录，可以是flow_1tuple_src_addr, Flow1Tuple_DstAddr, Flow2Tuple, flow_5tuple四种类型
            index (int): 哈希函数集合中的下标
        """
        if isinstance(flow_rec, Flow1Tuple_SrcAddr):
            if index >= cls.num_of_hashes_1tuple_srcIP:
                raise ValueError
            return cls.hashes_1tuple_srcIP[index]

        if isinstance(flow_rec, Flow1Tuple_DstAddr):
            if index >= cls.num_of_hashes_1tuple_dstIP:
                raise ValueError
            return cls.hashes_1tuple_dstIP[index]

        if isinstance(flow_rec, Flow2Tuple):
            if index >= cls.num_of_hashes_2tuple:
                raise ValueError
            return cls.hashes_2tuple[index]

        if isinstance(flow_rec, Flow5Tuple):
            if index >= cls.num_of_hashes_5tuple:
                raise ValueError
            return cls.hashes_5tuple[index]

        raise TypeError


# if __name__ == "__main__":
#     # a simple piece of test code
#     flow_list = FlowRecordList.read_groundtruth_file("no_dup_with_cnt_pkt.dat")
#     # flow_list = FlowRecordList.read_ground_truth("sent_flows.pickle")
#     flow_list.print_screen()


def typeof(variate):
    """判断输入对象的数据类型。

    Args:
        variate:　输入对象

    Returns:
        type (str): 输入对象的数据类型描述。
    """
    type_name = None
    if isinstance(variate, int):
        type_name = "int"
    elif isinstance(variate, str):
        type_name = "str"
    elif isinstance(variate, float):
        type_name = "float"
    elif isinstance(variate, list):
        type_name = "list"
    elif isinstance(variate, tuple):
        type_name = "tuple"
    elif isinstance(variate, dict):
        type_name = "dict"
    elif isinstance(variate, set):
        type_name = "set"
    return type_name


class RemoteSketchController(object):
    """能管理多个local controllers的remote controller类。
    """

    def __init__(self, controllers=None):
        self.controllers = []

        if controllers is not None:
            if isinstance(controllers, set) or isinstance(controllers, list) is False:
                print(typeof(controllers))
                print("Input parameter must be a list or a set of BasicSketchControllers")
                raise TypeError

            for c in controllers:
                if isinstance(c, BasicSketchController):
                    self.controllers.append(c);
                else:
                    print(typeof(c))
                    print("Each element in the input set must be a BasicSketchController")
                    raise TypeError

    def add_controller(self, controller):
        """为这个remote controller加一个要管理的local controller。

        Args:
            controller (BasicSketchController): 这个remote controller要管理的交换机的local controller。

        Returns:
            None
        """
        if not isinstance(controller, BasicSketchController):
            raise TypeError
        self.controllers.append(controller)
