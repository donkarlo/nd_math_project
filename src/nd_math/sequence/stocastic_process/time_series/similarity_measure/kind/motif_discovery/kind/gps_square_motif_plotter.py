import numpy as np
import matplotlib


def configure_matplotlib_backend() -> None:
    try:
        matplotlib.use("QtAgg")
        return
    except Exception:
        pass

    try:
        matplotlib.use("WebAgg")
        return
    except Exception:
        pass


configure_matplotlib_backend()

import matplotlib.pyplot as plt

from nd_sociomind.experiment.parts.oldest.uav1_300k_normal_time_position_modality import \
    Uav1300kNormalTimePositionModality


class GpsSquareMotifPlotter:
    def __init__(self, data_slice: slice, period_shift: int = 24525, corner_half_width: int = 300,
                 smoothing_window_size: int = 51, heading_lag: int = 25):
        self.data_slice = data_slice
        self.period_shift = period_shift
        self.corner_half_width = corner_half_width
        self.smoothing_window_size = smoothing_window_size
        self.heading_lag = heading_lag
        self.time_positions_composite_memory = None

    def run(self) -> None:
        gps_time_series = self._load_gps()
        projected_positions = self._project_to_two_dimensions(gps_time_series)

        first_period_positions = projected_positions[0:self.period_shift]
        second_period_positions = projected_positions[self.period_shift:self.period_shift * 2]

        if second_period_positions.shape[0] == 0:
            raise ValueError("Second period is empty. Increase the data slice or reduce period_shift.")

        corner_centers = self._detect_corner_centers(first_period_positions)
        shifted_positions, shifted_corner_centers, cycle_start_index = self._shift_period_to_start_after_last_corner(
            first_period_positions, corner_centers)
        segments = self._build_eight_segments(shifted_corner_centers, shifted_positions.shape[0])

        print(f"Matplotlib backend: {matplotlib.get_backend()}")
        print(f"GPS time series shape: {gps_time_series.shape}")
        print(f"Projected positions shape: {projected_positions.shape}")
        print(f"First period length: {first_period_positions.shape[0]}")
        print(f"Second period length: {second_period_positions.shape[0]}")
        print("Detected corner centers in original first period:")
        print(corner_centers)
        print(f"Cycle start index used for shifted plot: {cycle_start_index}")
        print("Shifted corner centers:")
        print(shifted_corner_centers)

        for segment_name, start_index, end_index in segments:
            print(f"{segment_name}: {start_index} -> {end_index}, length={end_index - start_index}")

        self._plot_period_overlay(first_period_positions, second_period_positions)
        self._plot_eight_segments(shifted_positions, segments)
        self._plot_curvature_score(first_period_positions, corner_centers)

        plt.show(block=True)

    def _load_gps(self) -> np.ndarray:
        self.time_positions_composite_memory = Uav1300kNormalTimePositionModality(self.data_slice)
        data = self.time_positions_composite_memory.get_np_positions()

        if data.ndim != 2:
            raise ValueError("Position data must have shape (time_steps, features).")

        if data.shape[1] < 3:
            raise ValueError("Position data must contain at least three columns: x, y, z.")

        gps_time_series = data[:, 0:3]
        gps_time_series = self._remove_nan_rows(gps_time_series)
        gps_time_series = self._center_gps_series(gps_time_series)

        return gps_time_series

    def _remove_nan_rows(self, gps_time_series: np.ndarray) -> np.ndarray:
        valid_rows = ~np.isnan(gps_time_series).any(axis=1)
        cleaned_time_series = gps_time_series[valid_rows]
        return cleaned_time_series

    def _center_gps_series(self, gps_time_series: np.ndarray) -> np.ndarray:
        first_position = gps_time_series[0]
        centered_time_series = gps_time_series - first_position
        return centered_time_series

    def _project_to_two_dimensions(self, gps_time_series: np.ndarray) -> np.ndarray:
        centered_positions = gps_time_series - np.mean(gps_time_series, axis=0)
        left_singular_vectors, singular_values, right_singular_vectors = np.linalg.svd(centered_positions,
                                                                                       full_matrices=False)
        projection_matrix = right_singular_vectors[0:2].T
        projected_positions = centered_positions @ projection_matrix
        return projected_positions

    def _smooth_positions(self, positions: np.ndarray) -> np.ndarray:
        window_size = self.smoothing_window_size

        if window_size < 3:
            return positions.copy()

        if window_size % 2 == 0:
            window_size = window_size + 1

        kernel = np.ones(window_size) / window_size
        smoothed_positions = np.zeros_like(positions)

        for dimension_index in range(positions.shape[1]):
            smoothed_positions[:, dimension_index] = np.convolve(positions[:, dimension_index], kernel, mode="same")

        return smoothed_positions

    def _calculate_curvature_score(self, positions: np.ndarray) -> np.ndarray:
        smoothed_positions = self._smooth_positions(positions)
        point_count = smoothed_positions.shape[0]
        lag = self.heading_lag

        if point_count <= 2 * lag + 2:
            raise ValueError("The period is too short for the selected heading lag.")

        previous_positions = smoothed_positions[0:point_count - 2 * lag]
        next_positions = smoothed_positions[2 * lag:point_count]
        direction_vectors = next_positions - previous_positions

        headings = np.unwrap(np.arctan2(direction_vectors[:, 1], direction_vectors[:, 0]))
        heading_changes = np.abs(np.diff(headings))

        curvature_score = np.zeros(point_count)
        start_index = lag + 1
        end_index = start_index + heading_changes.shape[0]
        curvature_score[start_index:end_index] = heading_changes

        curvature_score = self._smooth_one_dimensional_signal(curvature_score, self.smoothing_window_size)
        return curvature_score

    def _smooth_one_dimensional_signal(self, signal: np.ndarray, window_size: int) -> np.ndarray:
        if window_size < 3:
            return signal.copy()

        if window_size % 2 == 0:
            window_size = window_size + 1

        kernel = np.ones(window_size) / window_size
        smoothed_signal = np.convolve(signal, kernel, mode="same")
        return smoothed_signal

    def _detect_corner_centers(self, period_positions: np.ndarray) -> list[int]:
        curvature_score = self._calculate_curvature_score(period_positions)
        period_length = period_positions.shape[0]
        minimum_distance = period_length // 8

        ranked_indices = np.argsort(curvature_score)[::-1]
        selected_centers = []

        for candidate_index in ranked_indices:
            if candidate_index < self.corner_half_width:
                continue

            if candidate_index > period_length - self.corner_half_width - 1:
                continue

            if self._is_far_from_selected_centers(candidate_index, selected_centers, minimum_distance, period_length):
                selected_centers.append(int(candidate_index))

            if len(selected_centers) == 4:
                break

        selected_centers.sort()

        if len(selected_centers) != 4:
            raise ValueError(f"Expected 4 corners, but detected {len(selected_centers)} corners.")

        return selected_centers

    def _is_far_from_selected_centers(self, candidate_index: int, selected_centers: list[int], minimum_distance: int,
                                      period_length: int) -> bool:
        for selected_center in selected_centers:
            direct_distance = abs(candidate_index - selected_center)
            circular_distance = min(direct_distance, period_length - direct_distance)

            if circular_distance < minimum_distance:
                return False

        return True

    def _shift_period_to_start_after_last_corner(self, period_positions: np.ndarray, corner_centers: list[int]) -> \
    tuple[np.ndarray, list[int], int]:
        period_length = period_positions.shape[0]
        last_corner_center = corner_centers[-1]
        cycle_start_index = (last_corner_center + self.corner_half_width) % period_length

        shifted_positions = np.vstack([
            period_positions[cycle_start_index:period_length],
            period_positions[0:cycle_start_index]
        ])

        shifted_corner_centers = []

        for corner_center in corner_centers:
            shifted_center = (corner_center - cycle_start_index) % period_length
            shifted_corner_centers.append(int(shifted_center))

        shifted_corner_centers.sort()
        return shifted_positions, shifted_corner_centers, cycle_start_index

    def _build_eight_segments(self, shifted_corner_centers: list[int], period_length: int) -> list[
        tuple[str, int, int]]:
        segments = []
        current_start_index = 0

        for corner_index, corner_center in enumerate(shifted_corner_centers):
            straight_start_index = current_start_index
            straight_end_index = max(straight_start_index, corner_center - self.corner_half_width)

            if straight_end_index > straight_start_index:
                straight_name = f"Straight {corner_index + 1}"
                segments.append((straight_name, straight_start_index, straight_end_index))

            corner_start_index = max(0, corner_center - self.corner_half_width)
            corner_end_index = min(period_length, corner_center + self.corner_half_width)

            corner_name = f"Corner {corner_index + 1}"
            segments.append((corner_name, corner_start_index, corner_end_index))

            current_start_index = corner_end_index

        if current_start_index < period_length:
            segment_name = "Straight 4"
            segments.append((segment_name, current_start_index, period_length))

        if len(segments) != 8:
            print(f"Warning: expected 8 segments, but built {len(segments)} segments.")

        return segments

    def _plot_period_overlay(self, first_period_positions: np.ndarray, second_period_positions: np.ndarray) -> None:
        comparable_length = min(first_period_positions.shape[0], second_period_positions.shape[0])
        first_period_positions = first_period_positions[0:comparable_length]
        second_period_positions = second_period_positions[0:comparable_length]

        figure, axis = plt.subplots(figsize=(10, 8))
        axis.plot(first_period_positions[:, 0], first_period_positions[:, 1], linewidth=1.5, label="First period")
        axis.plot(second_period_positions[:, 0], second_period_positions[:, 1], linewidth=1.5, label="Second period")
        axis.scatter(first_period_positions[0, 0], first_period_positions[0, 1], s=60, label="First period start")
        axis.scatter(second_period_positions[0, 0], second_period_positions[0, 1], s=60, label="Second period start")
        axis.set_aspect("equal", adjustable="box")
        axis.grid(True)
        axis.legend()
        axis.set_title("Overlay of the two GPS periods")
        axis.set_xlabel("Projected axis 1")
        axis.set_ylabel("Projected axis 2")
        figure.tight_layout()

    def _plot_eight_segments(self, shifted_positions: np.ndarray, segments: list[tuple[str, int, int]]) -> None:
        figure, axis = plt.subplots(figsize=(10, 8))

        for segment_name, start_index, end_index in segments:
            segment_positions = shifted_positions[start_index:end_index]

            if segment_positions.shape[0] == 0:
                continue

            axis.plot(segment_positions[:, 0], segment_positions[:, 1], linewidth=2.0, label=segment_name)

            middle_index = segment_positions.shape[0] // 2
            label_x = segment_positions[middle_index, 0]
            label_y = segment_positions[middle_index, 1]
            axis.text(label_x, label_y, segment_name, fontsize=9)

        axis.scatter(shifted_positions[0, 0], shifted_positions[0, 1], s=70, label="Shifted period start")
        axis.set_aspect("equal", adjustable="box")
        axis.grid(True)
        axis.legend()
        axis.set_title("One period segmented into four straights and four corners")
        axis.set_xlabel("Projected axis 1")
        axis.set_ylabel("Projected axis 2")
        figure.tight_layout()

    def _plot_curvature_score(self, first_period_positions: np.ndarray, corner_centers: list[int]) -> None:
        curvature_score = self._calculate_curvature_score(first_period_positions)

        figure, axis = plt.subplots(figsize=(12, 4))
        axis.plot(curvature_score, linewidth=1.2, label="Curvature score")

        for corner_index, corner_center in enumerate(corner_centers):
            axis.axvline(corner_center, linestyle="--", label=f"Corner {corner_index + 1}")

        axis.grid(True)
        axis.legend()
        axis.set_title("Curvature score used for corner detection")
        axis.set_xlabel("Time index inside the first period")
        axis.set_ylabel("Absolute heading change")
        figure.tight_layout()


if __name__ == "__main__":
    plotter = GpsSquareMotifPlotter(
        data_slice=slice(0, 50000),
        period_shift=24525,
        corner_half_width=300,
        smoothing_window_size=51,
        heading_lag=25
    )

    plotter.run()