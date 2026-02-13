from typing import Union, Sequence
import numpy as np


class Tensor:
    "Defines the relation between tensors - if you inout this vector, it gives you that vector"
    def __init__(self, components: Union[Sequence[float], np.ndarray]):
        if not isinstance(components, np.ndarray):
            self._components = np.asarray(components)
        self._rank = self._components.ndim

    def get_rank(self) -> int:
        return self._rank