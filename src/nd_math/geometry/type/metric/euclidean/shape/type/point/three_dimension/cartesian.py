from nd_math.linear_algebra.tensor.vector.vector import Vector


class Cartesian(Vector):
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        super(Vector).__init__([self._x, self._y])

    def to_cartesian(self) -> "Cartesian":
        return self

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def change_origin(self, origin: Vector):
        pass
