from abc import abstractmethod, ABC

from nd_math.probability.distribution.distribution import Distribution


class Discrepancy(ABC):
    def __init__(self, distribution_one: Distribution, distribution_two: Distribution):
        self._distribution_one = distribution_one
        self._distribution_two = distribution_two

    @abstractmethod
    def get_discrepancy_value(self, distribution_one: Distribution, distribution_two: Distribution)->float:
        pass
