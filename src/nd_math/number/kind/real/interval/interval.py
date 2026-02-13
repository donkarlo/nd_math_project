from nd_math.number.kind.real.bound.bound import Bound


class Interval:
    def __init__(self, lowerbound: Bound, upperbound: Bound):
        self._lowerbound = lowerbound
        self._upperbound = upperbound

    def get_lowerbound(self) -> float:
        return self._lowerbound

    def get_upperbound(self) -> float:
        return self._upperbound

    def is_greater(self, val: float) -> bool:
        if self._lowerbound.get_val() > val:
            return False

    def is_smaller(self, val: float) -> bool:
        if self._lowerbound.get_val() < val:
            return False
