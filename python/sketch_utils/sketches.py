import random
from array import array
from random import randint
from math import log, e, ceil
from sketch_utils.basic_sketch import *
from sketch_utils.hash_functions import *


class CountMinSketch(BasicSketch):
    """
        Count min sketch.
    """

    def __init__(self, sketch_bucket_length):
        super().__init__()
        self.sketch_bucket_length = sketch_bucket_length
        self.sketch1 = [0 for _ in range(sketch_bucket_length)]
        self.sketch2 = [0 for _ in range(sketch_bucket_length)]
        self.sketch3 = [0 for _ in range(sketch_bucket_length)]
        self.sketch4 = [0 for _ in range(sketch_bucket_length)]
        self.sketches = [self.sketch1, self.sketch2, self.sketch3, self.sketch4]

    def __get_sketch_index(self, sketch_num, key):
        """
        get sketch index of key via HashEx32.  计算 key 在 sketch_num 中索引
        :param sketch_num:
        :param key:
        :return:
        """
        hash_holder = HashEx32(str(sketch_num))
        index = hash_holder.hash(str(key)) & (self.sketch_bucket_length - 1)
        # return hash_holder.hash(str(key)) & (self.sketch_bucket_length - 1)

        # index = hash(str(sketch_num+10) + str(key)) & (self.sketch_bucket_length - 1)
        # print(index)
        return index

    def _get_each_sketch_value(self, sketch_num, key):
        """
        get sketch value of key from sketch_num.  获取 key 在 sketch_num 中对应的 value
        :param sketch_num:
        :param key:
        :return:
        """
        if sketch_num != 1 and sketch_num != 2 and sketch_num != 3 and sketch_num != 4:
            value = None
        else:
            value = self.sketches[sketch_num - 1][self.__get_sketch_index(sketch_num, key)]

        return value

    def get_value(self, key):
        """
        here can be improved by SIMD
        get the count min value of key.
        :param key:
        :return:
        """
        value = self._get_each_sketch_value(1, key)
        for sketch_num in range(len(self.sketches) - 1):
            tmp = self._get_each_sketch_value(sketch_num + 2, key)
            if tmp < value:
                value = tmp
        # print(value)
        return value

    def _set_each_sketch_value(self, sketch_num, key, in_data):
        """
        set each sketch value of key.
        :param sketch_num:
        :param key:
        :param in_data:
        :return:
        """
        if sketch_num != 1 and sketch_num != 2 and sketch_num != 3 and sketch_num != 4:
            raise ValueError('the sketch_num is error!!!')

        self.sketches[sketch_num - 1][self.__get_sketch_index(sketch_num, key)] = in_data

    def set_value(self, key, in_data):
        """
        set the count min value of key
        :param key:
        :param in_data: value 的 增量
        :return:
        """
        for sketch_num in range(len(self.sketches)):
            value = self._get_each_sketch_value(sketch_num + 1, key)
            self._set_each_sketch_value(sketch_num + 1, key, value + in_data)

    def __show_all_sketch_value(self):
        """
        show every value in sektches
        :return:
        """
        for sketch_num in range(len(self.sketches)):
            print('sketch[' + str(sketch_num + 1) + ']: ')
            for index in range(self.sketch_bucket_length):
                print(str(self.sketches[sketch_num][index]) + ', ', end='')
            print('\n')

    def get_values(self):
        """
        :return: 返回 sketches
        """
        return self.sketches

    def show_values(self):
        self.__show_all_sketch_value()


class CountSketch(BasicSketch):
    """
        Count sketch.
    """

    def __init__(self, sketch_bucket_length):
        super().__init__()
        self.sketch_bucket_length = sketch_bucket_length
        self.sketch1 = [0 for _ in range(sketch_bucket_length)]
        self.sketch2 = [0 for _ in range(sketch_bucket_length)]
        self.sketch3 = [0 for _ in range(sketch_bucket_length)]
        self.sketch4 = [0 for _ in range(sketch_bucket_length)]
        self.sketches = [self.sketch1, self.sketch2, self.sketch3, self.sketch4]
        self.gsketch1 = [1 for _ in range(sketch_bucket_length)]
        self.gsketch2 = [1 for _ in range(sketch_bucket_length)]
        self.gsketch3 = [1 for _ in range(sketch_bucket_length)]
        self.gsketch4 = [1 for _ in range(sketch_bucket_length)]
        self.gsketches = [self.gsketch1, self.gsketch2, self.gsketch3, self.gsketch4]

    def __get_sketch_index(self, sketch_num, key):
        """
        sketch_num : 1 - 4
        HashEx32(str(sketch_num + seed))
        sketch_num + 0: CM sketches' hash seed
        sketch_num + 11: CS sketches' hash seed
        sketch_num + 19: CS gsketches' hash seed
        """
        hash_holder = HashEx32(str(sketch_num + 17))
        index = hash_holder.hash(str(key)) & (self.sketch_bucket_length - 1)
        # print(index)
        return index

    def _get_each_sketch_value(self, sketch_num, key):
        """
        get sketch value of key from sketch_num.
        :param sketch_num:
        :param key:
        :return:
        """
        if sketch_num != 1 and sketch_num != 2 and sketch_num != 3 and sketch_num != 4:
            value = None
        else:
            value = self.sketches[sketch_num - 1][self.__get_sketch_index(sketch_num, key)]

        return value

    def get_value(self, key):
        sketchlist = []
        for sketch_num in range(len(self.sketches)):
            tmp = self._get_each_sketch_value(sketch_num + 1, key) * self.gsketches[sketch_num][
                self.__get_sketch_index(sketch_num + 1, key)]
            sketchlist.append(tmp)
        sketchlist.sort()
        # value = (abs(sketchlist[1]) + abs(sketchlist[2])) / 2
        # value = sketchlist[1]
        value = (sketchlist[1] + sketchlist[2]) / 2
        print(value)
        return value

    def _set_each_sketch_value(self, sketch_num, key, in_data):
        """
        set each sketch value of key.
        :param sketch_num:
        :param key:
        :param in_data:
        :return:
        """
        if sketch_num != 1 and sketch_num != 2 and sketch_num != 3 and sketch_num != 4:
            raise ValueError('the sketch_num is error!!!')

        self.sketches[sketch_num - 1][self.__get_sketch_index(sketch_num, key)] = in_data

    def set_value(self, key, in_data):

        for sketch_num in range(len(self.gsketches)):
            ghash_holder = HashEx32(str(sketch_num + 129))
            ghash = ghash_holder.hash(str(key)) & (self.sketch_bucket_length - 1)
            g = 1
            if (ghash > self.sketch_bucket_length >> 1):
                g = 1
            else:
                g = -1
            self.gsketches[sketch_num][self.__get_sketch_index(sketch_num + 1, key)] = g
            value = self._get_each_sketch_value(sketch_num + 1, key)
            if g == -1:
                self._set_each_sketch_value(sketch_num + 1, key, value - in_data)
            else:
                self._set_each_sketch_value(sketch_num + 1, key, value + in_data)

        # for sketch_num in range(len(self.sketches)):
        #     value = self._get_each_sketch_value(sketch_num + 1, key)
        #     if(self.gsketches[sketch_num]) == 1):
        #         self._set_each_sketch_value(sketch_num + 1, key, value + in_data)
        #     else:
        #         self._set_each_sketch_value(sketch_num + 1, key, value - in_data)

    def __show_all_sketch_value(self):
        for sketch_num in range(len(self.sketches)):
            print('sketch[' + str(sketch_num + 1) + ']: ')
            for index in range(self.sketch_bucket_length):
                print(str(self.sketches[sketch_num][index]) + ', ', end='')
            print('\n')

    def get_values(self):
        return self.sketches

    def show_values(self):
        self.__show_all_sketch_value()


class MemoryDictionary(BasicSketch):
    def __init__(self):
        super().__init__()
        self.kvs = {}

    def set_value(self, key, in_data):
        self.kvs[key] = self.kvs.get(key, 0.0) + in_data

    def get_value(self, key):
        value = 0.0
        if key in self.kvs.keys():
            value = self.kvs[key]

        return value

    def get_values(self):
        return self.kvs

    def show_values(self):
        self._show_kvs_values()

    def _show_kvs_values(self):
        for k in self.kvs.keys():
            print('key: ' + str(k) + ', value: ' + str(self.kvs[k]), end='; ')


class MinHeap:
    def __init__(self, capacity, key):
        self.__capacity = capacity
        self.__data = []
        self.__data_map = {}
        self.__size = 0
        self.__key = key

    def get_capacity(self):
        return self.__capacity

    def get_key(self):
        return self.__key

    def size(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def __push_item(self, item):
        """
        往小顶堆中添加元素：
                添加规则：
                1. 首先把新添加的元素当做最后一个叶子节点添加到堆的最后面
                2. 判断当前节点和其父节点的大小：若当前节点小于父节点，那么交换两个节点的位置；然后继续往上比较，
                   直到当前节点大于其父节点（即在_shiftUp函数中实现的逻辑）
        :param item:
        :return:
        """
        self.__data.append(item)
        self.__data_map[item.get_id()] = self.__size
        self.__shift_up(self.__size)
        self.__size += 1

    def __do_push_with_out_check_contains(self, item):
        """
            往固定容量的小顶堆中添加元素：
            1. 首先判断堆内元素个数是否超出规定范围
                若未超出： 元素入堆;
                若超出：
                    若该元素小于等于堆顶元素，不入堆；
                    若该元素大于堆顶元素，入堆，同时删除小顶堆中最小元素（堆顶元素）。
            :param item: 需要加入到小顶堆中的元素
        """
        if self.__size < self.__capacity:
            self.__push_item(item)
        else:
            if self.__key(item) > self.__key(self.__data[0]):
                self.__push_item(item)
                self.pop()

    def __do_push_with_check_contains(self, item):
        """
        首先检查该元素 ID 是否已经存在于堆中：
            若存在，修改该ID的value，并相应的上移或下移；
            若不存在，则直接按照不检查元素ID的情况入堆。
        :param item:
        :return:
        """
        contains = self.contains(item.get_id())
        if contains:
            index = self.__get_index(item.get_id())
            target_item = self.__data[index]
            value, target_value = self.__key(item), self.__key(target_item)
            target_item.set_value(value)
            if value > target_value:
                self.__shift_down(index)
            elif value < target_value:
                self.__shift_up(index)
        else:
            self.__do_push_with_out_check_contains(item)

    def push(self, item, check=True):
        if check:
            self.__do_push_with_check_contains(item)
        else:
            self.__do_push_with_out_check_contains(item)

    def __shift_up(self, index):
        parent_index = (index - 1) >> 1
        while index > 0 and self.__key(self.__data[index]) < self.__key(self.__data[parent_index]):
            # 当前节点不是根节点，并且当前节点的值小于其父节点，那么把当前节点和其父节点进行交换
            self.__swap(index, parent_index)
            index = parent_index
            parent_index = (index - 1) >> 1

    def pop(self):
        """
            1. 从小顶堆中弹出根节点，该元素肯定是这个堆中最小的元素；
            2. 调整堆的结构使得新的堆仍是一个最大堆：
                2.1 首先弹出根节点（也就是索引为0的元素），然后把最后一个叶子节点放到根节点位置
                2.2. 从根节点开始，比较其与两个子节点的大小：当当前节点大于其子节点时，则将当前节点与较小的一个子节点交换位置，
                     然后继续往下比较，直到当前节点是叶子节点或者当前节点小于子节点
            :return: 返回调整前最小堆中的最小值（即根节点）
        """
        if self.__size > 0:
            ret = self.__data[0]
            self.__data_map.pop(ret.get_id())
            self.__data[0] = self.__data[-1]
            self.__data_map[self.__data[0].get_id()] = 0
            self.__size -= 1
            self.__shift_down(0)
            self.__data = self.__data[0:-1]
            return ret

    def peek(self):
        if self.__size > 0:
            return self.__data[0]

    def __shift_down(self, index):
        # min_child最开始的左子节点
        min_child_index = (index << 1) + 1
        while min_child_index < self.__size:
            # 若右子节点存在 且 右子节点的值小于左节点的值，那么min_child = 右子节点
            if min_child_index + 1 < self.__size and self.__key(self.__data[min_child_index + 1]) < self.__key(
                    self.__data[min_child_index]):
                min_child_index = min_child_index + 1
            if self.__key(self.__data[index]) <= self.__key(self.__data[min_child_index]):
                break

            self.__swap(index, min_child_index)
            index = min_child_index
            min_child_index = (index << 1) + 1

    def __swap(self, index1, index2):
        self.__data[index1], self.__data[index2] = self.__data[index2], self.__data[index1]
        self.__data_map[self.__data[index1].get_id()] = index1
        self.__data_map[self.__data[index2].get_id()] = index2

    def get_all(self):
        return self.__data

    def contains(self, node_id):
        return node_id in self.__data_map.keys()

    def __get_index(self, node_id):
        return self.__data_map[node_id]
