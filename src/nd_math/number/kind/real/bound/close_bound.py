from nd_math.numbers.kind.real.bound.bound import Bound


class CloseBound(Bound):
    def __init__(self, value: float):
        super().__init__(value, False)
