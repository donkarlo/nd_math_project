from nd_math.probability.distribution.distribution import Distribution
import numpy as np

class Posterior(Distribution):
    def __init__(self, likelihood:Liklihood, prior):
        """
        prior:      p(x)           shape (N,)
        likelihood: p(z | x)       shape (N,)
        returns:    p(x | z)       shape (N,)
        """
        unnormalized_posterior = likelihood * prior
        normalization_constant = np.sum(unnormalized_posterior)
        return unnormalized_posterior / normalization_constant