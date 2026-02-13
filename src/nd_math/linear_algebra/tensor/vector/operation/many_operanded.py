import numpy as np
from typing import List
from nd_math.linear_algebra.tensor.vector.vector import Vector


class ManyOperanded:
    def __init__(self, vec_list: List[Vector]):
        # store a list of Vector objects
        self._vec_list = vec_list

    def get_concated(self) -> Vector:
        # concatenate components from all Vecs into a single Vector
        if not self._vec_list:
            raise ValueError("The vector list is empty.")

        # top with the components of the first Vector
        concated = self._vec_list[0].get_components()

        # concatenate the rest
        for vec in self._vec_list[1:]:
            concated = np.concatenate((concated, vec.get_components()))

        return Vector(concated)
