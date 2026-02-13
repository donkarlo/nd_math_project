from nd_math.probability.statistic.population.population import Population
from abc import ABC, abstractmethod
from typing import Iterable

from nd_math.probability.statistic.population.sampling.sampler.size.size import Size


class Sampler(ABC):
    """
    Sampler is a better name because it covers both Sample(Size), Sampler
    """
    def __init__(self, population:Population, size:Size):
        self._population = population
        self._size = size

        self._samples = None

    @abstractmethod
    def _build_samples(self) -> Iterable:
        pass

    def get_samples(self)->Iterable:
        if self._samples is None:
            self._build_samples()
        return self._samples

    def get_population(self):
        return self._population

    def get_size(self)->Size:
        return self._size

