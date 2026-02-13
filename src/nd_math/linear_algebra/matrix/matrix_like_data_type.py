from typing import Union, Annotated,List,Tuple
import numpy.typing as npt
import array
import numpy as np

MatrixLikeDataType = Union[
    Annotated[npt.NDArray[np.float64], ("n", "m")],  # NumPy 2D
    Annotated[List[List[float]], ("n", "m")],  # list of lists
    Annotated[Tuple[Tuple[float, ...], ...], ("n", "m")],  # tuple of tuples
    Annotated[Tuple[npt.NDArray[np.float64], ...], ("n", "m")],  # tuple of NumPy arrays
    Annotated[List[array.array], ("n", "m")],  # list of array.array (Python's built-in)
    Annotated[Tuple[array.array, ...], ("n", "m")]  # tuple of array.array
]
