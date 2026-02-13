from typing import Union, Sequence
import numpy as np

from nd_math.linear_algebra.tensor.vector.vector import Vector


class Row(Vector):
    '''
    The main responsibility of this class is to represent column vector form of a vector.
    Np.ndarray usually uses rows to show vectors but mathmaticians usually use the cilumn form
    '''

    def __init__(self, components: Union[Vector, Sequence[float], np.ndarray]):
        """

        Args:
            components:
        """

        if isinstance(components, Vector):
            components = components.get_components()
        elif isinstance(components, (list, tuple)):
            components = np.asarray(components)

        super().__init__(components)
        self._row_components = self._components.reshape(1, -1)

    def extend_vertically(self, extension: "Row") -> None:
        self._row_components = np.hstack((self._row_components, extension.get_col_components()))

    def get_row_components(self) -> np.ndarray:
        return self._row_components
