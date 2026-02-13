from abc import ABC, abstractmethod

from nd_math.probability.distribution.discrepancy.discrepancy import Discrepancy
from nd_math.probability.distribution.distribution import Distribution


class Divergence(Discrepancy, ABC):
    """
    It an asymmetric function to assess the information difference between two probability distributions
    """

    def __init__(self):
        Discrepancy.__init__(self)

    @abstractmethod
    def get_divergence_value(self, distribution_one: Distribution, distribution_two: Distribution) -> float:
        pass

    def get_discrepancy_value(self, distribution_one: Distribution, distribution_two: Distribution) -> float:
        self.get_divergence_value(distribution_one, distribution_two)
