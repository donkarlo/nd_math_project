import numpy as np
from nd_math.linear_algebra.tensor.vector.vector import Vector


class TwoOpranded:
    def __init__(self, left_vec: Vector, right_vec: Vector):
        self._left_vec = left_vec
        self._right_vec = right_vec

    def concat(self) -> Vector:
        """
        Concatenate left and right vectors into a new Vector.
        """
        combined = np.concatenate((
            self._left_vec.get_components(),
            self._right_vec.get_components()
        ))
        return Vector(combined)
