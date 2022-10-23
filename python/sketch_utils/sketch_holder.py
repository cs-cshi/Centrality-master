from sketch_utils.sketches import *


class SketchHolder:
    """
    This class hold the sketch values.
    """

    def __init__(self, sketch, min_heap=None):
        self.__sketch = sketch
        self.__min_heap = min_heap

    def get_sketch(self):
        return self.__sketch

    def get_min_heap(self):
        return self.__min_heap

    def get_sketch_value(self, key):
        return self.__sketch.get_value(key)

    def set_sketch_value(self, key, in_data):
        return self.__sketch.set_value(key, in_data)

    def show_values(self):
        self.__sketch.show_values()

    def get_values(self):
        return self.__sketch.get_values()

    def min_heap_get_peek(self):
        return self.__min_heap.peek()

    def min_heap_push(self, item):
        self.__min_heap.push(item)

    def min_heap_pop(self):
        return self.__min_heap.pop()

    def min_heap_get_all(self):
        return self.__min_heap.get_all()

    def min_heap_size(self):
        return self.__min_heap.size()

    def min_heap_is_empty(self):
        return self.__min_heap.is_empty()
