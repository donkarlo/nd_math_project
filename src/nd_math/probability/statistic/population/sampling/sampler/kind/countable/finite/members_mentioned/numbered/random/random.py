from nd_math.probability.statistic.population.kind.countable.finite.member_mentioned.numbered.numbered import \
    Numbered as NumberedPopulation
from nd_math.probability.statistic.population.sampling.sampler.kind.countable.finite.members_mentioned.numbered.numbered import Numbered as NumberedSampler
from nd_math.probability.statistic.population.sampling.sampler.sampler import Sampler
import numpy as np
from nd_math.probability.statistic.population.sampling.sampler.size.size import Size
from typing import Iterable

class Random(NumberedSampler):
    """
    Simplest random number taking
    """
    def __init__(self, population: NumberedPopulation, size: Size):
        """
        This sampler doesnt shuffle and
        Args:
            sample_size_ratio:

        Returns:

        """
        Sampler.__init__(self, population, size)


    def _build_samples(self) -> None:
        sample_size_value = self.get_size().get_value()
        population_members = self.get_population().get_members()

        population_size = self.get_population().get_size()
        all_indices = np.arange(population_size)

        subset_indices = np.random.choice(population_size, size=sample_size_value, replace=False)
        subset_indices = np.sort(subset_indices)

        complement_indices = np.setdiff1d(all_indices, subset_indices)

        self._samples = population_members[subset_indices]
        self._complements = population_members[complement_indices]

    def get_complements(self) -> Iterable:
        return self._complements