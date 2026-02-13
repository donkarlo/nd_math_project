from typing import Union, Sequence
import numpy as np

from nd_math.linear_algebra.tensor.vector.vector import Vector


class Column(Vector):
    '''
    The main responsibility of this class is to represent column vector form of a vector.
    Np.ndarray usually uses rows to show vectors but mathmaticians usually use the cilumn form
    - self._components.reshape(-1, 1)
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
        self._col_components = self._components.reshape(-1, 1)

    def extend_vertically(self, extension: "Column") -> None:
        self._col_components = np.vstack((self._col_components, extension.get_col_components()))

    def get_col_components(self) -> np.ndarray:
        return self._col_components
