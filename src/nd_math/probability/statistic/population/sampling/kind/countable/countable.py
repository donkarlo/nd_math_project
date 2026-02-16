from nd_math.probability.statistic.population.sampling.sampling import Sampling
from nd_math.probability.statistic.population.kind.countable.countable import Countable
from nd_math.probability.statistic.population.sampling.size.size import Size

class Countable(Sampling):
    def __init__(self, population: Countable, size:Size):
        Sampling.__init__(self, population, size)