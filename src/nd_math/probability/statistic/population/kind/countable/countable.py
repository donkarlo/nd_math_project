from nd_math.probability.statistic.population.population import Population
from collections.abc import Iterable

class Countable(Population):
    def __init__(self, members: Iterable):
        if not isinstance(members, Iterable):
            raise TypeError('members must be a iterable')
        Population.__init__(self, members)