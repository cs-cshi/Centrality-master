import math


class WeightFunction:
    def __int__(self):
        pass

    def get_weight(self, weight, base=None):
        pass


class LogFunction(WeightFunction):
    def __init__(self, base=None):
        self.__base = base

    def get_weight(self, weight):
        return self.__log(weight)

    def __log(self, weight):
        if self.__base is None:
            value = math.log(weight)
        else:
            value = math.log(1 + float(weight), self.__base)

        return value
