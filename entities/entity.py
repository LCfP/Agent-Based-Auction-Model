from collections import defaultdict


class Entity(object):

    def __init__(self):
        self._lookup = defaultdict(lambda: 0)

    def __getattribute__(self, item):
        object.__getattribute__(self, "_lookup")[item] += 1

        return object.__getattribute__(self, item)
