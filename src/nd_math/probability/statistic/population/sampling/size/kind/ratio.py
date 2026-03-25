from nd_math.number.kind.real.interval.unit.close_unit_interval import CloseUnitInterval
from nd_math.probability.statistic.population.sampling.size.size import Size


class Ratio(Size):
    def __init__(self, ratio: CloseUnitInterval, population_length:int):
        self._ratio = ratio
        self._size_value = int(self._ratio.get_value() * population_length)
        Size.__init__(self, self._size_value)

    def get_ratio(self):
        return self._ratio