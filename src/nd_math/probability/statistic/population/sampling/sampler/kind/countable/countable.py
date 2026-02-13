from nd_math.probability.statistic.population.sampling.sampler.sampler import Sampler
from nd_math.probability.statistic.population.kind.countable.countable import Countable
from nd_math.probability.statistic.population.sampling.sampler.size.size import Size

class Countable(Sampler):
    def __init__(self, population: Countable, size:Size):
        Sampler.__init__(self, population, size)