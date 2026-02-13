from nd_math.probability.statistic.population.interface import Interface as PopulationInterface
from typing import Any


class Population(PopulationInterface):
    """
    Here they are exclusively numerical populations
    - example:
        - All men over 185cm
    - we usually dont have allmembers of a population
    - we show the siz by capital N
    """
    def __init__(self, members):
        self._members = members

    def get_members(self)->Any:
        return self._members