from typing import Any

from nd_math.set.set import Set


class Countable(Set):
    def __init__(self, members:Any):
        Set.__init__(self, members)