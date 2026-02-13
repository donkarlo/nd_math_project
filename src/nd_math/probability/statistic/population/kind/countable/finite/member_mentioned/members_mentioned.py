from nd_math.probability.statistic.population.kind.countable.finite.finite import Finite
from typing import Iterable

class MembersMentioned(Finite):
    def __init__(self, members:Iterable) -> None:
        Finite.__init__(self, members)