from nd_math.linear_algebra.tensor.vector.vector import Vector
from nd_math.probability.distribution.parametricity.kind.parametric.covariance_matrix import CovarianceMatrix
from nd_math.probability.distribution.continuity.continuous.continuous import Continuous
from nd_math.probability.distribution.parametricity.kind.parametric.parametric import Parametric


class Gaussian(Continuous, Parametric):
    def __init__(self, mean: Vector, covariance_matrix: CovarianceMatrix):
        self._mean = mean
        self._covariance_matrix = covariance_matrix
        Parametric.__init__(self, (self._mean, self._covariance_matrix))

    def get_mean(self) -> Vector:
        return self._mean

    def get_covariance_matrix(self) -> CovarianceMatrix:
        return self._covariance_matrix
