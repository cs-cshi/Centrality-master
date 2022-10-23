from model.node_definitions import *
from .basic_computer import *


class AdaKatzComputerParams:
    def __init__(self, beta, time_amplify_function, weight_function=None):
        if 0 <= beta <= 1:
            self._beta = beta
        else:
            raise RuntimeError("the beta must be from interval [0, 1]!")
        self._time_amplify_function = time_amplify_function
        self._weight_function = weight_function

    def get_beta(self):
        return self._beta

    def get_time_amplify_function(self):
        return self._time_amplify_function

    def set_beta(self, beta):
        self._beta = beta

    def set_time_amplify_function(self, time_amplify_function):
        self._time_amplify_function = time_amplify_function

    def set_weight_function(self, weight_function):
        self._weight_function = weight_function

    def get_weight_function(self):
        return self._weight_function


# 读/写 sketch值时 引入time-adaptive思想 去加权/加权
class AdaKatzComputer(BasicComputer):
    def __init__(self, sketch_holder, params):
        super().__init__(sketch_holder)
        self.__params = params

    def get_params(self):
        return self.__params

    def get_updated_node_rank(self, node_id, time):
        sketch_rank_value = self._sketch_holder.get_sketch_value(node_id)
        # updated_node_rank is zero if node did not appear before
        updated_node_rank = 0
        if sketch_rank_value != 0:
            updated_node_rank = self.sketch_value_to_rank(sketch_rank_value, time)
        return updated_node_rank

    # def update(self, src_node_id, dst_node_id, src_time, dst_time):
    def update(self, src_node_id, dst_node_id, time):
        src_rank = self.get_updated_node_rank(src_node_id, time)
        dst_rank = self.get_updated_node_rank(dst_node_id, time) + self.__params.get_beta() * (src_rank + 1)
        # print('src_centrality: ' + str(src_rank) + ', dst_centrality: ' + str(dst_rank))

        if self._sketch_holder.get_min_heap() is not None:
            self._sketch_holder.min_heap_push(Node(src_node_id, src_rank))
            self._sketch_holder.min_heap_push(Node(dst_node_id, dst_rank))

        self._sketch_holder.set_sketch_value(src_node_id, self.rank_to_sketch_value(src_rank, time))
        self._sketch_holder.set_sketch_value(dst_node_id, self.rank_to_sketch_value(dst_rank, time))

    def ada_update(self, src_node_id, dst_node_id, time, weight=None):
        src_sketch_value = self._sketch_holder.get_sketch_value(src_node_id)
        src_rank_value = self.sketch_value_to_rank(src_sketch_value, time)
        increment = self.get_increment(src_rank_value, weight)
        # print(increment)

        # get count-min value
        dst_sketch_value = self._sketch_holder.get_sketch_value(
            dst_node_id) + increment * self.__params.get_time_amplify_function().amplify(time)

        if self._sketch_holder.get_min_heap() is not None:
            # self._sketch_holder.min_heap_push(Node(src_node_id, src_rank_value))
            self._sketch_holder.min_heap_push(Node(dst_node_id, dst_sketch_value))

        self._sketch_holder.set_sketch_value(dst_node_id,
                                             increment * self.__params.get_time_amplify_function().amplify(time))

    def get_increment(self, src_rank_value, weight=None):
        increment = (src_rank_value + 1) * self.__params.get_beta()
        if weight is not None:
            increment = increment * self.__params.get_weight_function().get_weight(weight)

        return increment

    def rank_to_sketch_value(self, value, time):
        return value * self.__params.get_time_amplify_function().amplify(time)

    def sketch_value_to_rank(self, value, time):
        return value / self.__params.get_time_amplify_function().amplify(time)

    def save_snapshot(self):
        pass


