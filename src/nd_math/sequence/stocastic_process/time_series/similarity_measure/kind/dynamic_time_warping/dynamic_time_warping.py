from collections.abc import Sequence
from math import inf
from math import sqrt

TimeSeriesPoint = float | int | Sequence[float | int]


class EuclideanPointDistance:
    def calculate(self, first_point: TimeSeriesPoint, second_point: TimeSeriesPoint) -> float:
        if isinstance(first_point, int | float) and isinstance(second_point, int | float):
            return abs(float(first_point) - float(second_point))

        if isinstance(first_point, int | float) or isinstance(second_point, int | float):
            raise ValueError("Both points must have the same structure.")

        if len(first_point) != len(second_point):
            raise ValueError("Both points must have the same number of dimensions.")

        squared_distance = 0.0

        for dimension_index in range(len(first_point)):
            difference = float(first_point[dimension_index]) - float(second_point[dimension_index])
            squared_distance = squared_distance + difference * difference

        return sqrt(squared_distance)


class DynamicTimeWarpingResult:
    def __init__(self, distance: float, accumulated_cost_matrix: list[list[float]],
                 alignment_path: list[tuple[int, int]]) -> None:
        self.distance = distance
        self.accumulated_cost_matrix = accumulated_cost_matrix
        self.alignment_path = alignment_path

    def get_distance(self) -> float:
        return self.distance

    def get_accumulated_cost_matrix(self) -> list[list[float]]:
        return self.accumulated_cost_matrix

    def get_alignment_path(self) -> list[tuple[int, int]]:
        return self.alignment_path


class DynamicTimeWarpingCalculator:
    def __init__(self, point_distance_calculator: EuclideanPointDistance | None = None) -> None:
        if point_distance_calculator is None:
            self.point_distance_calculator = EuclideanPointDistance()
        else:
            self.point_distance_calculator = point_distance_calculator

    def calculate(self, first_time_series: Sequence[TimeSeriesPoint],
                  second_time_series: Sequence[TimeSeriesPoint]) -> DynamicTimeWarpingResult:
        self.validate_time_series(first_time_series)
        self.validate_time_series(second_time_series)

        accumulated_cost_matrix = self.build_accumulated_cost_matrix(first_time_series, second_time_series)
        distance = accumulated_cost_matrix[len(first_time_series)][len(second_time_series)]
        alignment_path = self.build_alignment_path(accumulated_cost_matrix)

        return DynamicTimeWarpingResult(distance, accumulated_cost_matrix, alignment_path)

    def validate_time_series(self, time_series: Sequence[TimeSeriesPoint]) -> None:
        if len(time_series) == 0:
            raise ValueError("Time series must not be empty.")

    def build_accumulated_cost_matrix(self, first_time_series: Sequence[TimeSeriesPoint],
                                      second_time_series: Sequence[TimeSeriesPoint]) -> list[list[float]]:
        first_length = len(first_time_series)
        second_length = len(second_time_series)

        accumulated_cost_matrix = []

        for row_index in range(first_length + 1):
            row = []

            for column_index in range(second_length + 1):
                row.append(inf)

            accumulated_cost_matrix.append(row)

        accumulated_cost_matrix[0][0] = 0.0

        for first_index in range(1, first_length + 1):
            for second_index in range(1, second_length + 1):
                local_distance = self.point_distance_calculator.calculate(first_time_series[first_index - 1],
                                                                          second_time_series[second_index - 1])

                insertion_cost = accumulated_cost_matrix[first_index - 1][second_index]
                deletion_cost = accumulated_cost_matrix[first_index][second_index - 1]
                match_cost = accumulated_cost_matrix[first_index - 1][second_index - 1]

                minimum_previous_cost = min(insertion_cost, deletion_cost, match_cost)

                accumulated_cost_matrix[first_index][second_index] = local_distance + minimum_previous_cost

        return accumulated_cost_matrix

    def build_alignment_path(self, accumulated_cost_matrix: list[list[float]]) -> list[tuple[int, int]]:
        first_index = len(accumulated_cost_matrix) - 1
        second_index = len(accumulated_cost_matrix[0]) - 1

        alignment_path = []

        while first_index > 0 or second_index > 0:
            alignment_path.append((first_index - 1, second_index - 1))

            if first_index == 0:
                second_index = second_index - 1
            elif second_index == 0:
                first_index = first_index - 1
            else:
                diagonal_cost = accumulated_cost_matrix[first_index - 1][second_index - 1]
                vertical_cost = accumulated_cost_matrix[first_index - 1][second_index]
                horizontal_cost = accumulated_cost_matrix[first_index][second_index - 1]

                if diagonal_cost <= vertical_cost and diagonal_cost <= horizontal_cost:
                    first_index = first_index - 1
                    second_index = second_index - 1
                elif vertical_cost <= horizontal_cost:
                    first_index = first_index - 1
                else:
                    second_index = second_index - 1

        alignment_path.reverse()

        return alignment_path


if __name__ == "__main__":
    first_time_series = [1.0, 2.0, 3.0, 4.0, 5.0]
    second_time_series = [1.0, 1.8, 2.7, 3.5, 5.0]

    calculator = DynamicTimeWarpingCalculator()
    result = calculator.calculate(first_time_series, second_time_series)

    print("DTW distance:", result.get_distance())
    print("Alignment path:", result.get_alignment_path())
