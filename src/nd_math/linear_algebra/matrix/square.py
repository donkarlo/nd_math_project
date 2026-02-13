from nd_math.linear_algebra.matrix.matrix_like_data_type import MatrixLikeDataType
from nd_math.linear_algebra.tensor.vector.vector import Vector
from nd_math.linear_algebra.matrix.matrix import Matrix
import numpy as np

class Square(Matrix):
    def __init__(self, components: MatrixLikeDataType):
        Matrix.__init__(self, components)
        if not self.is_square():
            raise ValueError("Expected a square components")

    def is_symmetric(self) -> bool:
        return np.array_equal(self._components, self._components.T)

    # Approximate check (optional helper)
    def is_symmetric_approx(self, atol: float = 1e-12, rtol: float = 0.0) -> bool:
        return np.allclose(self._components, self._components.T, atol=atol, rtol=rtol)

    def is_psd(self, tol: float = 1e-12) -> bool:
        """positive semi definit"""
        if not self.is_symmetric():
            return False
        w = np.linalg.eigvalsh(self._components)
        return np.min(w) >= -tol

    def is_spd(self) -> bool:
        """Symmetric positive definite (SPD)."""
        if not self.is_symmetric():
            return False
        try:
            np.linalg.cholesky(self._components)
            return True
        except np.linalg.LinAlgError:
            return False

    def project_to_nearest_spd(self, jitter_start: float = 1e-12, max_tries: int = 12) -> "Square":
        eps = jitter_start
        S = 0.5 * (self._components + self._components.T)
        for _ in range(max_tries):
            try:
                np.linalg.cholesky(S + eps * np.eye(S.shape[0]))
                return Square(S + eps * np.eye(S.shape[0]))
            except np.linalg.LinAlgError:
                eps *= 10.0
        raise ValueError("Cannot project matrix to SPD")

    def determinant(self) -> float:
        return float(np.linalg.det(self._components))

    def inverse(self) -> "Square":
        return Square(np.linalg.inv(self._components))

    def get_diagonal(self) -> Vector:
        return Vector(np.diag(self._components))
