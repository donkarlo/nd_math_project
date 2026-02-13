import numpy as np
import numpy.typing as npt

type ScalarType = int | float | np.integer | np.floating
type TensorType = ScalarType | npt.NDArray[np.number]

class ForceType:
    @staticmethod
    def force_scalar_type(value: ScalarType):
        pass