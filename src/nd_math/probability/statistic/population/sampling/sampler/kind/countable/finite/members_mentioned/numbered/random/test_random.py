from nd_math.probability.statistic.population.kind.countable.finite.member_mentioned.numbered.numbered import Numbered as NumberedPopulation
import numpy as np
from nd_math.number.kind.real.interval.unit.open_unit_interval import OpenUnitInterval

from nd_math.probability.statistic.population.sampling.sampler.kind.countable.finite.members_mentioned.numbered.random.random import Random as RandomSampler
from nd_math.probability.statistic.population.sampling.sampler.size.kind.ratio import Ratio


class TestRandom:
    def setup_method(self):
        self._numbered_set = np.array([
            [1, 2],
            [2, 3],
            [3, 1],
            [4, 2],
            [5, 3],
            [3, 4],
            [2, 5],
            [4, 4],
            [10, 10],
            [11, 9],
            [12, 11],
            [13, 10],
            [14, 12],
            [15, 11],
            [16, 13],
            [17, 12],
            [18, 14],
            [19, 13],
            [20, 15],
            [21, 14],
            [22, 16],
            [23, 15],
            [24, 17],
        ])
        self._population = NumberedPopulation(self._numbered_set)

        size = Ratio(OpenUnitInterval(0.7), self._population.get_size())
        self._sampler = RandomSampler(self._population, size)

        self._samples = self._sampler.get_samples()
        self._complements = self._sampler.get_complements()

    def test_random_sample_and_complement_by_ratio(self)->None:
        for subset_member in self._samples:
            assert not np.any(np.all(self._complements == subset_member, axis=1))

    def test_order_keeping(self) -> None:
        population = self._population.get_members()

        last_found_index = -1

        for sample_member in self._samples:
            # find the first occurrence AFTER the previous one
            found = False
            for i in range(last_found_index + 1, len(population)):
                if np.array_equal(population[i], sample_member):
                    last_found_index = i
                    found = True
                    break

            assert found, "Sample member not found in population after previous index"




