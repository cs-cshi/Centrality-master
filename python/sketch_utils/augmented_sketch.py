from sketches import CountMinSketch
from sketches import MinHeap


class AugmentedSketch:
    """
    讲封装 count min sketch、MinHeap 封装成 Augmented_sketch
    """

    def __init__(self, cmsketch, filter):
        self.__count_min_sketch = cmsketch
        self.__filter = filter
