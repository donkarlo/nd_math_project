from nd_math.probability.statistic.population.sampling.sampler.kind.countable.countable import Countable
from nd_math.probability.statistic.population.kind.countable.finite.finite import Finite
from nd_math.probability.statistic.population.sampling.sampler.size.size import Size


class Finite(Countable):
    def __init__(self, population:Finite, size:Size):
        Countable.__init__(self, population, size)
