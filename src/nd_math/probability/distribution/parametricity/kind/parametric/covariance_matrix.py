from nd_math.linear_algebra.matrix.matrix import Matrix
from nd_math.linear_algebra.matrix.square import Square as SquareMatrix
from nd_math.linear_algebra.matrix.matrix_like_data_type import MatrixLikeDataType
from nd_math.linear_algebra.tensor.vector.vector import Vector
import numpy as np


class CovarianceMatrix(SquareMatrix):
    def __init__(self, components: MatrixLikeDataType, validate: bool):
        super().__init__(components)
        if validate:
            self.__validate()

    def __validate(self):
        if not self.is_symmetric():
            raise ValueError("Covariance matrix must be symmetric")

        if not self.is_psd():
            raise ValueError("Covariance matrix must be positive semidefinite (PSD)")

    def get_variances(self) -> Vector:
        """Return the diagonal (variances)."""
        return self.get_diagonal()

    def get_std(self) -> Vector:
        """Return the standard deviations."""
        return Vector(np.sqrt(self.get_variances().get_components()))

    def get_correlation_matrix(self) -> Matrix:
        """Return the normalized correlation matrix."""
        std = self.get_std().get_components()
        D_inv = np.diag(1.0 / np.maximum(std, 1e-12))
        corr = D_inv @ self._components @ D_inv
        return Matrix(corr)

    def satisfies_cauchy_schwarz(self, tol: float = 1e-9) -> bool:
        """Check |cov_ij| <= sqrt(var_i * var_j)."""
        vars_ = self.get_variances().get_components()
        for i in range(len(vars_)):
            for j in range(i + 1, len(vars_)):
                bound = np.sqrt(vars_[i] * vars_[j])
                if abs(self._components[i, j]) - bound > tol:
                    return False
        return True

    def cholesky_with_jitter(self, jitter_start: float = 1e-12, max_tries: int = 12) -> np.ndarray:
        """
        Try Cholesky; if it fails, add increasing jitter to the diagonal.
        Returns lower-triangular L such that (Σ + jitter I) = L L^T.
        """
        jitter = jitter_start
        for _ in range(max_tries):
            try:
                return np.linalg.cholesky(self._components + jitter * np.eye(self.get_rows_count()))
            except np.linalg.LinAlgError:
                jitter *= 10.0
        raise np.linalg.LinAlgError("Cholesky failed even after jittering.")

    def nearest_psd(self, eps: float = 0.0) -> "CovarianceMatrix":
        """
        Project to the nearest PSD by clipping eigenvalues below eps (>= 0).
        This is a 'repair' method, so we symmetrize inside intentionally.
        """
        A = 0.5 * (self._components + self._components.T)
        w, V = np.linalg.eigh(A)
        w = np.maximum(w, eps)
        A_psd = V @ np.diag(w) @ V.T
        # Return validated instance (exact symmetry + PSD)
        return CovarianceMatrix(A_psd, validate=True)
