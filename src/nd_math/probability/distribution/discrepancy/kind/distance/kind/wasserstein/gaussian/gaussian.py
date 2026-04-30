import numpy as np


class Gaussian(Distance):
    def __init__(self, numerical_tolerance: float = 1e-10):
        self._numerical_tolerance = numerical_tolerance

    def calculate_distance(self, first_mean: np.ndarray, first_covariance: np.ndarray, second_mean: np.ndarray,
                           second_covariance: np.ndarray) -> float:
        first_mean = self._convert_to_vector(first_mean)
        second_mean = self._convert_to_vector(second_mean)

        first_covariance = self._convert_to_matrix(first_covariance)
        second_covariance = self._convert_to_matrix(second_covariance)

        mean_distance_squared = self._calculate_euclidean_distance_squared(first_mean, second_mean)
        covariance_distance_squared = self._calculate_covariance_distance_squared(first_covariance, second_covariance)

        distance_squared = mean_distance_squared + covariance_distance_squared

        if distance_squared < 0 and abs(distance_squared) < self._numerical_tolerance:
            distance_squared = 0.0

        return float(np.sqrt(distance_squared))

    def calculate_direction(self, first_mean: np.ndarray, second_mean: np.ndarray) -> np.ndarray:
        first_mean = self._convert_to_vector(first_mean)
        second_mean = self._convert_to_vector(second_mean)

        direction = first_mean - second_mean

        return direction

    def _calculate_euclidean_distance_squared(self, first_mean: np.ndarray, second_mean: np.ndarray) -> float:
        difference = first_mean - second_mean

        return float(difference.T @ difference)

    def _calculate_covariance_distance_squared(self, first_covariance: np.ndarray,
                                               second_covariance: np.ndarray) -> float:
        second_covariance_square_root = self._calculate_symmetric_matrix_square_root(second_covariance)

        inner_matrix = second_covariance_square_root @ first_covariance @ second_covariance_square_root
        inner_matrix_square_root = self._calculate_symmetric_matrix_square_root(inner_matrix)

        covariance_term = np.trace(first_covariance + second_covariance - 2.0 * inner_matrix_square_root)

        if covariance_term < 0 and abs(covariance_term) < self._numerical_tolerance:
            covariance_term = 0.0

        return float(covariance_term)

    def _calculate_symmetric_matrix_square_root(self, matrix: np.ndarray) -> np.ndarray:
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)

        clipped_eigenvalues = np.clip(eigenvalues, 0.0, None)
        square_root_eigenvalues = np.sqrt(clipped_eigenvalues)

        square_root_matrix = eigenvectors @ np.diag(square_root_eigenvalues) @ eigenvectors.T

        return square_root_matrix

    def _convert_to_vector(self, value: np.ndarray) -> np.ndarray:
        converted_value = np.asarray(value, dtype=float)
        converted_value = converted_value.reshape(-1)

        return converted_value

    def _convert_to_matrix(self, value: np.ndarray) -> np.ndarray:
        converted_value = np.asarray(value, dtype=float)

        if converted_value.ndim == 0:
            converted_value = converted_value.reshape(1, 1)

        if converted_value.ndim == 1:
            converted_value = np.diag(converted_value)

        return converted_value