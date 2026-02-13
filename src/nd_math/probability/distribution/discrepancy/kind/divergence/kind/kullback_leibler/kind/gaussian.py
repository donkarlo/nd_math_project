import numpy as np

from nd_math.probability.distribution.discrepancy.discrepancy import Discrepancy
from nd_math.probability.distribution.discrepancy.kind.divergence.kind.kullback_leibler.kullback_leibler import \
    KullbackLeiblerDivergence
from nd_utility.oop.inheritance.overriding.override_from import override_from
from nd_math.probability.distribution.kind.gaussian.gaussian import Gaussian as GaussianDistribution


class Gaussian(KullbackLeiblerDivergence):
    def __init__(self):
        KullbackLeiblerDivergence.__init__(self)

    @override_from(Discrepancy, False, False)
    def get_divergence_value(self, distribution_one: GaussianDistribution, distribution_two: GaussianDistribution) -> float:
        # KL( N0 || N1 ) where:
        # N0 = distribution_one (mu0, Sigma0)
        # N1 = distribution_two (mu1, Sigma1)

        mean_one = distribution_one.get_mean().get_components().reshape(-1)
        mean_two = distribution_two.get_mean().get_components().reshape(-1)

        covariance_one_components = distribution_one.get_covariance_matrix().get_components()
        covariance_two = distribution_two.get_covariance_matrix().get_components()

        dimension = int(mean_one.shape[0])

        sign_two, log_det_two = np.linalg.slogdet(covariance_two)
        sign_one, log_det_one = np.linalg.slogdet(covariance_one_components)

        if sign_two <= 0 or sign_one <= 0:
            raise ValueError("Covariance matrices must be symmetric positive definite (determinant must be positive)")

        # trace(Sigma1^{-1} Sigma0)
        trace_term = float(np.trace(np.linalg.solve(covariance_two, covariance_one_components)))

        # (mu1 - mu0)^T Sigma1^{-1} (mu1 - mu0)
        mean_difference = (mean_two - mean_one).reshape(dimension, 1)
        quadratic_term = float((mean_difference.T @ np.linalg.solve(covariance_two, mean_difference)).item())

        # log(det(Sigma1) / det(Sigma0))
        log_det_ratio = float(log_det_two - log_det_one)

        kl_value = 0.5 * (log_det_ratio - dimension + trace_term + quadratic_term)
        return float(kl_value)
