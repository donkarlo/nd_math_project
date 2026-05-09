import numpy as np
import matplotlib

try:
    matplotlib.use("QtAgg")
except Exception:
    try:
        matplotlib.use("WebAgg")
    except Exception:
        pass

import matplotlib.pyplot as plt

from nd_sociomind.experiment.parts.oldest.uav1_300k_normal_time_position_modality import \
    Uav1300kNormalTimePositionModality


class GpsSquareLabeledCirclePlotter:
    def __init__(self, data_slice: slice, period_shift: int = 24525, corner_half_width: int = 300,
                 smoothing_window_size: int = 51, heading_lag: int = 25, circles_per_side: int = 20,
                 circle_size: int = 55, label_font_size: int = 8):
        self.data_slice = data_slice
        self.period_shift = period_shift
        self.corner_half_width = corner_half_width
        self.smoothing_window_size = smoothing_window_size
        self.heading_lag = heading_lag
        self.circles_per_side = circles_per_side
        self.circle_size = circle_size
        self.label_font_size = label_font_size
        self.time_positions_composite_memory = None

    def run(self) -> None:
        gps_time_series = self._load_gps()
        projected_positions = self._project_to_two_dimensions(gps_time_series)
        first_period_positions = projected_positions[0:self.period_shift]

        corner_centers = self._detect_corner_centers(first_period_positions)
        shifted_positions, shifted_corner_centers, cycle_start_index = self._shift_period_to_start_after_last_corner(
            first_period_positions, corner_centers)
        side_paths = self._build_side_paths_from_corner_centers(shifted_positions, shifted_corner_centers)

        print(f"Matplotlib backend: {matplotlib.get_backend()}")
        print(f"GPS time series shape: {gps_time_series.shape}")
        print(f"Projected positions shape: {projected_positions.shape}")
        print(f"First period length: {first_period_positions.shape[0]}")
        print(f"Original corner centers: {corner_centers}")
        print(f"Cycle start index: {cycle_start_index}")
        print(f"Shifted corner centers: {shifted_corner_centers}")

        for side_name, side_path in side_paths:
            print(f"{side_name}: point count={side_path.shape[0]}")

        self._plot_side_circles(shifted_positions, side_paths)
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

    def _build_side_paths_from_corner_centers(self, shifted_positions: np.ndarray, shifted_corner_centers: list[int]) -> \
    list[tuple[str, np.ndarray]]:
        period_length = shifted_positions.shape[0]
        first_corner = shifted_corner_centers[0]
        second_corner = shifted_corner_centers[1]
        third_corner = shifted_corner_centers[2]
        fourth_corner = shifted_corner_centers[3]

        side_1_path = np.vstack([
            shifted_positions[fourth_corner:period_length],
            shifted_positions[0:first_corner + 1]
        ])

        side_2_path = shifted_positions[first_corner:second_corner + 1]
        side_3_path = shifted_positions[second_corner:third_corner + 1]
        side_4_path = shifted_positions[third_corner:fourth_corner + 1]

        side_paths = [
            ("Side 1", side_1_path),
            ("Side 2", side_2_path),
            ("Side 3", side_3_path),
            ("Side 4", side_4_path)
        ]

        return side_paths

    def _plot_side_circles(self, shifted_positions: np.ndarray, side_paths: list[tuple[str, np.ndarray]]) -> None:
        figure, axis = plt.subplots(figsize=(12, 9))

        axis.plot(
            shifted_positions[:, 0],
            shifted_positions[:, 1],
            linewidth=1.2,
            color="black",
            alpha=0.35,
            label="GPS trajectory"
        )

        red_number_counter = 1
        white_number_counter = 1
        global_circle_index = 0
        has_added_red_legend = False
        has_added_white_legend = False

        for side_name, side_path in side_paths:
            if side_path.shape[0] < 2:
                continue

            circle_points, dense_values, tangent_vectors, normal_vectors = self._sample_corner_dense_points_tangents_normals_on_path(
                side_path, self.circles_per_side)

            middle_point = circle_points[circle_points.shape[0] // 2]
            axis.text(middle_point[0], middle_point[1], side_name, fontsize=10)

            for local_index in range(circle_points.shape[0]):
                circle_point = circle_points[local_index]
                dense_value = dense_values[local_index]
                tangent_vector = tangent_vectors[local_index]
                normal_vector = normal_vectors[local_index]

                if global_circle_index % 2 == 0:
                    face_color = "red"
                    circle_label = self._get_circle_legend_label(face_color, has_added_red_legend,
                                                                 has_added_white_legend)
                    number_text = str(red_number_counter)
                    red_number_counter = red_number_counter + 1

                    if red_number_counter > 10:
                        red_number_counter = 1

                    has_added_red_legend = True
                else:
                    face_color = "white"
                    circle_label = self._get_circle_legend_label(face_color, has_added_red_legend,
                                                                 has_added_white_legend)
                    number_text = str(white_number_counter)
                    white_number_counter = white_number_counter + 1

                    if white_number_counter > 10:
                        white_number_counter = 1

                    has_added_white_legend = True

                axis.scatter(
                    circle_point[0],
                    circle_point[1],
                    s=self.circle_size,
                    facecolors=face_color,
                    edgecolors="black",
                    linewidths=0.9,
                    zorder=6,
                    label=circle_label
                )

                label_position = self._calculate_number_label_position(circle_point, tangent_vector, normal_vector,
                                                                       dense_value, local_index)
                axis.text(
                    label_position[0],
                    label_position[1],
                    number_text,
                    fontsize=self.label_font_size,
                    ha="center",
                    va="center",
                    zorder=7
                )

                global_circle_index = global_circle_index + 1

        axis.set_aspect("equal", adjustable="box")
        axis.grid(True)
        axis.legend()
        axis.set_title("Alternating derivative circles on GPS square sides")
        axis.set_xlabel("Projected axis 1")
        axis.set_ylabel("Projected axis 2")
        figure.tight_layout()

    def _get_circle_legend_label(self, face_color: str, has_added_red_legend: bool,
                                 has_added_white_legend: bool) -> str | None:
        if face_color == "red":
            if has_added_red_legend:
                return None
            else:
                return "0th derivative (consonant)"

        if has_added_white_legend:
            return None
        else:
            return "1st derivative (vowel)"

    def _sample_corner_dense_points_tangents_normals_on_path(self, path_positions: np.ndarray, point_count: int) -> \
    tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        arc_lengths = self._calculate_arc_lengths(path_positions)
        total_length = arc_lengths[-1]

        if total_length <= 1e-12:
            repeated_points = np.repeat(path_positions[0:1], point_count, axis=0)
            repeated_dense_values = np.linspace(0.0, 1.0, point_count, endpoint=False)
            repeated_tangents = np.repeat(np.array([[1.0, 0.0]]), point_count, axis=0)
            repeated_normals = np.repeat(np.array([[0.0, 1.0]]), point_count, axis=0)
            return repeated_points, repeated_dense_values, repeated_tangents, repeated_normals

        uniform_values = np.linspace(0.0, 1.0, point_count, endpoint=False)
        dense_values = self._create_corner_dense_values(uniform_values)
        target_lengths = dense_values * total_length

        sampled_points = []
        sampled_tangents = []
        sampled_normals = []

        for target_length in target_lengths:
            interpolated_point, tangent_vector, normal_vector = self._interpolate_point_tangent_normal_by_arc_length(
                path_positions, arc_lengths, target_length)
            sampled_points.append(interpolated_point)
            sampled_tangents.append(tangent_vector)
            sampled_normals.append(normal_vector)

        return np.array(sampled_points), dense_values, np.array(sampled_tangents), np.array(sampled_normals)

    def _calculate_arc_lengths(self, path_positions: np.ndarray) -> np.ndarray:
        differences = np.diff(path_positions, axis=0)
        segment_lengths = np.sqrt(np.sum(differences ** 2, axis=1))
        arc_lengths = np.zeros(path_positions.shape[0])
        arc_lengths[1:] = np.cumsum(segment_lengths)
        return arc_lengths

    def _create_corner_dense_values(self, uniform_values: np.ndarray) -> np.ndarray:
        dense_values = 0.5 - 0.5 * np.cos(np.pi * uniform_values)
        return dense_values

    def _interpolate_point_tangent_normal_by_arc_length(self, path_positions: np.ndarray, arc_lengths: np.ndarray,
                                                        target_length: float) -> tuple[
        np.ndarray, np.ndarray, np.ndarray]:
        upper_index = int(np.searchsorted(arc_lengths, target_length, side="left"))

        if upper_index <= 0:
            lower_index = 0
            upper_index = 1
        elif upper_index >= arc_lengths.shape[0]:
            upper_index = arc_lengths.shape[0] - 1
            lower_index = upper_index - 1
        else:
            lower_index = upper_index - 1

        lower_length = arc_lengths[lower_index]
        upper_length = arc_lengths[upper_index]

        if upper_length - lower_length <= 1e-12:
            interpolation_ratio = 0.0
        else:
            interpolation_ratio = (target_length - lower_length) / (upper_length - lower_length)

        interpolated_point = (1.0 - interpolation_ratio) * path_positions[lower_index] + interpolation_ratio * \
                             path_positions[upper_index]

        tangent_vector = path_positions[upper_index] - path_positions[lower_index]
        tangent_norm = np.linalg.norm(tangent_vector)

        if tangent_norm <= 1e-12:
            tangent_unit_vector = np.array([1.0, 0.0])
        else:
            tangent_unit_vector = tangent_vector / tangent_norm

        normal_vector = np.array([-tangent_unit_vector[1], tangent_unit_vector[0]])

        return interpolated_point, tangent_unit_vector, normal_vector

    def _calculate_number_label_position(self, circle_point: np.ndarray, tangent_vector: np.ndarray,
                                         normal_vector: np.ndarray, dense_value: float, local_index: int) -> np.ndarray:
        distance_to_nearest_corner = min(dense_value, 1.0 - dense_value)
        corner_proximity = 1.0 - 2.0 * distance_to_nearest_corner

        if corner_proximity < 0.0:
            corner_proximity = 0.0

        normal_offset = 0.16 + 0.65 * corner_proximity
        tangent_offset = 0.04 + 0.35 * corner_proximity

        if local_index % 2 == 0:
            normal_sign = 1.0
        else:
            normal_sign = -1.0

        if local_index % 4 < 2:
            tangent_sign = 1.0
        else:
            tangent_sign = -1.0

        label_position = circle_point + normal_sign * normal_offset * normal_vector + tangent_sign * tangent_offset * tangent_vector
        return label_position


if __name__ == "__main__":
    plotter = GpsSquareLabeledCirclePlotter(
        data_slice=slice(0, 50000),
        period_shift=24525,
        corner_half_width=300,
        smoothing_window_size=51,
        heading_lag=25,
        circles_per_side=20,
        circle_size=55,
        label_font_size=8
    )

    plotter.run()