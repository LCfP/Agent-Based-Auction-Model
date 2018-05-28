from collections import defaultdict


class Entity(object):

    def __init__(self, env):
        self._lookup = defaultdict(lambda: 0)
        self.env = env

    def __getattribute__(self, item):
        env = object.__getattribute__(self, "env")

        if env.day > env.config.warmup_period:
            object.__getattribute__(self, "_lookup")[item] += 1

        return object.__getattribute__(self, item)
