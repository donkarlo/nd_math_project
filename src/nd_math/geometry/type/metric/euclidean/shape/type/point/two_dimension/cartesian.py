from nd_math.linear_algebra.tensor.vector.vector_representable import VectorRepresentable


class Cartesian(VectorRepresentable):
    def __init__(self, x:float, y:float, z:float):
        self._x = x
        self._y = y
        self._z = z

    def to_cartesian(self) -> "Cartesian":
        return self

    def get_x(self) -> float:
        return self._x

    def get_y(self) -> float:
        return self._y

    def get_z(self) -> float:
        return self._z

    def change_origin(self, origin: Vec):
        pass
