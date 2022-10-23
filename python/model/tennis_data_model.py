class Mention:
    def __init__(self, src, dst, timestamp):
        self._src = src
        self._dst = dst
        self._timestamp = timestamp

    def get_src(self):
        return self._src

    def get_dst(self):
        return self._dst

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def __repr__(self):
        return str(self._src) + ' ' + str(self._dst) + ' ' + str(self._timestamp)
