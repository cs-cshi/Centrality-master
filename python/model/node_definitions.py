class Node:
    def __init__(self, node_id, rank=0.0):
        self.__node_id = node_id
        self.__rank = rank

    def get_rank(self):
        return self.__rank

    def get_node_id(self):
        return self.__node_id

    def set_node_id(self, node_id):
        self.__node_id = node_id

    def set_rank(self, rank):
        self.__rank = rank

    def get_value(self):
        return self.__rank

    def set_value(self, value):
        self.__rank = value

    def get_id(self):
        return self.__node_id

    def __repr__(self):
        return 'node_id: ' + str(self.__node_id) + ', rank: ' + str(self.__rank)
