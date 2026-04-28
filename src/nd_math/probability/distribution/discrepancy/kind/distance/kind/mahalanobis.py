from nd_math.probability.distribution.discrepancy.kind.distance.distance import Distance
import numpy as np


class Mahalanobis(Distance):
    def __init__(self):
        Distance.__init__(self)

    def get_distance_value(self, population_one: np.ndarray, population_two: np.ndarray) -> float:
        """
        - if you give two scalars then it will give the absolute value
        - if you give two vectors, it will give the Euclidean distance
        - population one and two must be finit data points
        Args:
            population_one:
            population_two:

        Returns:

        """
        # case 1: two single points -> Euclidean distance
        if population_one.ndim == 1 and population_two.ndim == 1:
            delta = population_one - population_two
            return float(np.sqrt(delta @ delta))

        # case 2: two populations -> Mahalanobis distance between means
        mean_one = np.mean(population_one, axis=0)
        mean_two = np.mean(population_two, axis=0)
        delta = mean_one - mean_two

        pooled = np.vstack([population_one, population_two])
        covariance = np.cov(pooled, rowvar=False)

        distance_squared = float(delta.T @ np.linalg.inv(covariance) @ delta)
        return float(np.sqrt(distance_squared))
