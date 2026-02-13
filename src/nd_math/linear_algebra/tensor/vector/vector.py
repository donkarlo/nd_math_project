from nd_math.linear_algebra.tensor.tensor import Tensor
from nd_math.linear_algebra.tensor.vector.vector_representable import VectorRepresentable
from typing import Union, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from nd_math.linear_algebra.tensor.vector.row import Row
    from nd_math.linear_algebra.tensor.vector.column import Column

import numpy as np


class Vector(Tensor):
    def __init__(self, components: Union[Sequence[float], np.ndarray]) -> None:
        """
        - Vector is something that has start point and direction and length. Do not mistake a point with a vector. You can use vector to represent a point, in this case, it's start point is the origin of the carthesian axis and the direction and the length takes us to the point. SO a vector says how to go to the point from the origini and it is not the point itself. Dont over use this class for representations.
        Vector holds an array of shape (n,).
        You can convert it into a row or column vector when needed.
        - Vector is direction+magnititude, do not mistake it with point
        """
        self.__init(components)

    def set_components(self, components: Union[Sequence[float], np.ndarray]) -> None:
        self.__init(components)

    def __init(self, components: Union[Sequence[float], np.ndarray, VectorRepresentable]) -> None:
        #this line is for the time we want for example Vector(Position) work correctly
        if isinstance(components, VectorRepresentable):
            components = components.get_vector_representation().get_components()
            return

        components = np.asarray(components, dtype=float)
        if components.ndim != 1:
            raise ValueError(f"Expected a flat 1D vector, got shape {self._components.shape}")
        self._components = components
        self._components_len = self._components.shape[0]
        Tensor.__init__(self, self._components)

    def get_components(self) -> np.ndarray:
        """
        Return the vector as a flat array of shape (n,).
        """
        return self._components

    def __getitem__(self, item) -> float:
        return self._components[item]

    def get_dimension(self) -> int:
        return self._components_len

    def get_row_vector(self) -> "Row":
        """
        Return the vector as a row vector of shape (1, n).
        """
        from nd_math.linear_algebra.tensor.vector.row import Row
        return Row(self)

    def get_column_vector(self) -> "Column":
        """
        Return the vector as a column vector of shape (n, 1).
        """
        from nd_math.linear_algebra.tensor.vector.col import Column
        return Column(self)
