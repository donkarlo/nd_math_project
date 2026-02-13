from nd_math.probability.statistic.population.kind.countable.countable import Countable
from typing import Iterable

class Finite(Countable):
    def __init__(self, members: Iterable):
        Countable.__init__(self, members)

    def get_size(self) -> int:
        return len(self._members)