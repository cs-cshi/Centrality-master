from centrality_computer.basic_computer import *
from model.node_definitions import *


class TemporalKatzParams:
    def __init__(self, beta, weight_function):
        if 0 <= beta <= 1:
            self.__beta = beta
        else:
            raise RuntimeError("'beta' must be from interval [0,1]!")
        self.__weight_function = weight_function

    def get_beta(self):
        return self.__beta

    def set_beta(self, beta):
        self.__beta = beta

    def get_weight_function(self):
        return self.__weight_function

    def set_weight_function(self, weight_function):
        self.__weight_function = weight_function


# 最初的temporal katz算法，存储方式可选择cm cs或者直接存（minheap)
# 没有time-adaptive sketch的加权/去加权
class TemporalKatzComputer(BasicComputer):
    """General temporal Katz centrality implementation"""

    def __init__(self, sketch_holder, params):
        super().__init__(sketch_holder)
        self.__params = params
        self.__node_last_activation = {}

    def get_params(self):
        return self.__params

    def get_node_last_activation(self):
        return self.__node_last_activation

    def get_updated_node_rank(self, node_id, time):
        updated_rank = self._sketch_holder.get_sketch_value(node_id)  # zero value if node did not appear before
        if node_id in self.__node_last_activation:
            delta_time = time - self.__node_last_activation[node_id]
            time_decaying_weight = self.__params.get_weight_function().weight(-delta_time)
            updated_rank *= time_decaying_weight
        return updated_rank

    def update(self, src, dst, time):
        src_rank = self.get_updated_node_rank(src, time)
        dst_rank = self.get_updated_node_rank(dst, time) + self.__params.get_beta() * (src_rank + 1)
        if self._sketch_holder.get_min_heap() is not None:
            self._sketch_holder.min_heap_push(Node(src, src_rank))
            self._sketch_holder.min_heap_push(Node(dst, dst_rank))
        self._sketch_holder.set_sketch_value(src, src_rank)
        self._sketch_holder.set_sketch_value(dst, dst_rank)
        self.__node_last_activation[src] = time
        self.__node_last_activation[dst] = time
