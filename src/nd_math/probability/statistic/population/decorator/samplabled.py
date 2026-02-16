from nd_math.probability.statistic.population.decorator.decorator import Decorator
from nd_math.probability.statistic.population.interface import Interface
from nd_math.probability.statistic.population.sampling.sampling import Sampling
from typing import Any

class Samplabled(Decorator):
    def __init__(self, inner:Interface, sampler:Sampling):
        Decorator.__init__(self, inner)
        self._sampler = sampler
    def get_samples(self)->Any:
        return self._sampler.get_samples()