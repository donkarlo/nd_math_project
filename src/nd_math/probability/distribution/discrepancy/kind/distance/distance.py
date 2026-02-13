from nd_math.probability.distribution.discrepancy.discrepancy import Discrepancy
from abc import ABC, abstractmethod

from nd_math.probability.distribution.distribution import Distribution


class Distance(Discrepancy, ABC):
    def __init__(self):
        Discrepancy.__init__(self)

    @abstractmethod
    def get_distance_value(self, distribution_one: Distribution, distribution_two: Distribution) -> float:
        pass

    def get_discrepancy_value(self, distribution_one: Distribution, distribution_two: Distribution) -> float:
        self.get_distance_value(distribution_one, distribution_two)
