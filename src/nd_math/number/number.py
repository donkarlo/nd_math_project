import numpy as np
from  math.number.type_hint.type_hint import TENSOR

class Number:
    def ensure_numeric(self, x: Tensor) -> None:
        if isinstance(x, np.ndarray):
            if not np.issubdtype(x.dtype, np.number):
                raise TypeError("Array must be numeric")