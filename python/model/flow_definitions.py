class Flow:
    def __init__(self, src, dst, timestamp, length):
        self.__src = src
        self.__dst = dst
        self.__timestamp = timestamp
        self.__length = length

    def get_src(self):
        return self.__src

    def get_dst(self):
        return self.__dst

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_length(self):
        return self.__length

    def __repr__(self):
        return self.__src + ' ' + self.__dst + ' ' + str(self.__timestamp) + ' ' + self.__length


class FlowRecords:
    def __init__(self, records=None):
        if records is None:
            records = []
        self._records = records

    def get_records(self):
        return self._records

    def set_records(self, records):
        self._records = records
