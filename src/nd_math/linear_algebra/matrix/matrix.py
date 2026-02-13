from typing import Tuple

import numpy as np


class Matrix:
    def __init__(self, components: np.ndarray):
        if not self.__is_valid_2d():
            raise TypeError("Expected a 2D array-like structure (n × m)")
        self._components = np.asarray(components)

    def get_dimension_shape(self) -> Tuple[int, int]:
        return self._components.shape

    def get_dims_with_multi_sign(self) -> str:
        rows, cols = self._components.shape
        return f"{rows} × {cols}"

    def transpose(self) -> "Matrix":
        """Return a new Matrix object that is the transpose of this one."""
        transposed_data = self._components.T
        return Matrix(transposed_data)

    def __is_valid_2d(self) -> bool:
        try:
            arr = np.asarray(self._components)
            return arr.ndim == 2
        except Exception:
            return False

    def transpose(self) -> "Matrix":
        return Matrix(self._components.T)

    def is_square(self) -> bool:
        return self._components.shape[0] == self._components.shape[1]

    def pinv(self, rcond: float = 1e-15) -> "Matrix":
        """Moore-Penrose pseudoinverse via SVD; works for any shape."""
        return Matrix(np.linalg.pinv(self._components, rcond=rcond))

    def rank(self, tol: float | None = None) -> int:
        """Numerical rank via SVD; works for any shape."""
        s = np.linalg.svd(self._components, compute_uv=False)
        if tol is None:
            tol = max(self._rows, self._cols) * np.finfo(float).eps * np.max(s)
        return int(np.sum(s > tol))

    def gram_AtA(self) -> "Matrix":
        """A^T A (square, symmetric, PSD)."""
        return Matrix(self._components.T @ self._components)

    def gram_AAt(self) -> "Matrix":
        """A A^T (square, symmetric, PSD)."""
        return Matrix(self._components @ self._components.T)

    def get_rows_count(self) -> int:
        return self.get_dimension_shape()[0]

    def get_columns_count(self) -> int:
        return self.get_dimension_shape()[1]

    def get_components(self) -> np.ndarray:
        return self._components
