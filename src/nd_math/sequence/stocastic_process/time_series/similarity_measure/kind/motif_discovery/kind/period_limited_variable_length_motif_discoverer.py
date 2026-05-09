import numpy as np

from motif_candidate import MotifCandidate


class PeriodLimitedVariableLengthMotifDiscoverer:
    def __init__(self, window_size: int, distance_threshold: float, minimum_shift: int, maximum_shift: int,
                 shift_step: int = 1, scale_cap: float = 4.0, max_event_gap: int = 5, minimum_event_count: int = 5,
                 maximum_motifs: int = 20):
        self.window_size = window_size
        self.distance_threshold = distance_threshold
        self.minimum_shift = minimum_shift
        self.maximum_shift = maximum_shift
        self.shift_step = shift_step
        self.scale_cap = scale_cap
        self.max_event_gap = max_event_gap
        self.minimum_event_count = minimum_event_count
        self.maximum_motifs = maximum_motifs

    def discover(self, time_series: np.ndarray) -> list[MotifCandidate]:
        self._validate_time_series(time_series)

        time_series = time_series.astype(np.float32, copy=False)

        print("Building normalized windows...")
        normalized_windows, window_scales = self._build_normalized_windows(time_series)

        motif_candidates = []
        shift_values = list(range(self.minimum_shift, self.maximum_shift + 1, self.shift_step))

        print(f"Window count: {normalized_windows.shape[0]}")
        print(f"Shift count: {len(shift_values)}")

        for shift_index, diagonal_shift in enumerate(shift_values):
            print(f"Processing shift {shift_index + 1}/{len(shift_values)}: {diagonal_shift}")

            if diagonal_shift >= normalized_windows.shape[0]:
                continue

            distance_values = self._calculate_diagonal_distances(normalized_windows, window_scales, diagonal_shift)
            event_indices = np.flatnonzero(distance_values <= self.distance_threshold).tolist()
            event_groups = self._group_event_indices(event_indices)

            print(f"Events: {len(event_indices)}, event groups: {len(event_groups)}")

            for event_group in event_groups:
                motif_candidate = self._build_candidate(time_series, event_group, diagonal_shift)

                if motif_candidate is None:
                    continue

                motif_candidates.append(motif_candidate)

        print(f"Raw motif candidates: {len(motif_candidates)}")

        motif_candidates.sort(key=lambda candidate: (-candidate.event_count, candidate.distance, -candidate.length))
        selected_candidates = self._remove_overlapping_candidates(motif_candidates)

        return selected_candidates[:self.maximum_motifs]

    def _validate_time_series(self, time_series: np.ndarray) -> None:
        if time_series.ndim != 2:
            raise ValueError("The time series must have shape (time_steps, features).")

        if time_series.shape[1] < 3:
            raise ValueError("The GPS time series must contain at least three columns: x, y, z.")

        if time_series.shape[0] <= self.maximum_shift + self.window_size:
            raise ValueError("The time series is too short for the selected shift range and window size.")

    def _build_normalized_windows(self, time_series: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        windows = np.lib.stride_tricks.sliding_window_view(time_series, window_shape=self.window_size, axis=0)
        windows = np.transpose(windows, (0, 2, 1))

        mean_values = np.mean(windows, axis=1, keepdims=True)
        standard_deviation_values = np.std(windows, axis=1, keepdims=True)

        safe_standard_deviation_values = standard_deviation_values.copy()
        safe_standard_deviation_values[safe_standard_deviation_values < 1e-12] = 1.0

        normalized_windows = (windows - mean_values) / safe_standard_deviation_values
        normalized_windows = normalized_windows.astype(np.float32, copy=False)

        window_standard_deviations = np.std(windows, axis=1)
        window_scales = np.sqrt(np.mean(window_standard_deviations ** 2, axis=1))
        window_scales = window_scales.astype(np.float32, copy=False)

        return normalized_windows, window_scales

    def _calculate_diagonal_distances(self, normalized_windows: np.ndarray, window_scales: np.ndarray,
                                      diagonal_shift: int) -> np.ndarray:
        available_window_count = normalized_windows.shape[0] - diagonal_shift

        first_windows = normalized_windows[0:available_window_count]
        second_windows = normalized_windows[diagonal_shift:diagonal_shift + available_window_count]

        difference_values = first_windows - second_windows
        raw_shape_distances = np.sqrt(np.sum(difference_values ** 2, axis=(1, 2)))

        feature_count = normalized_windows.shape[2]
        normalized_shape_distances = raw_shape_distances / (2.0 * np.sqrt(self.window_size * feature_count))

        first_scales = window_scales[0:available_window_count]
        second_scales = window_scales[diagonal_shift:diagonal_shift + available_window_count]

        scale_distances = self._calculate_scale_distances(first_scales, second_scales)
        final_distances = np.sqrt(normalized_shape_distances ** 2 + scale_distances ** 2) / np.sqrt(2.0)

        return final_distances

    def _calculate_scale_distances(self, first_scales: np.ndarray, second_scales: np.ndarray) -> np.ndarray:
        smaller_scales = np.minimum(first_scales, second_scales)
        larger_scales = np.maximum(first_scales, second_scales)

        raw_scale_distances = np.zeros_like(smaller_scales, dtype=np.float32)
        valid_indices = smaller_scales >= 1e-12
        raw_scale_distances[valid_indices] = larger_scales[valid_indices] / smaller_scales[valid_indices] - 1.0

        capped_scale_distances = np.minimum(raw_scale_distances, self.scale_cap) / self.scale_cap
        return capped_scale_distances

    def _group_event_indices(self, event_indices: list[int]) -> list[list[int]]:
        if len(event_indices) == 0:
            return []

        groups = []
        current_group = [event_indices[0]]

        for event_index in event_indices[1:]:
            previous_event_index = current_group[-1]

            if event_index - previous_event_index <= self.max_event_gap + 1:
                current_group.append(event_index)
            else:
                if len(current_group) >= self.minimum_event_count:
                    groups.append(current_group)

                current_group = [event_index]

        if len(current_group) >= self.minimum_event_count:
            groups.append(current_group)

        return groups

    def _build_candidate(self, time_series: np.ndarray, event_group: list[int],
                         diagonal_shift: int) -> MotifCandidate | None:
        first_start_index = event_group[0]
        second_start_index = first_start_index + diagonal_shift

        candidate_length = event_group[-1] - event_group[0] + self.window_size

        if candidate_length > diagonal_shift:
            candidate_length = diagonal_shift

        if second_start_index + candidate_length > time_series.shape[0]:
            return None

        first_subsequence = time_series[first_start_index:first_start_index + candidate_length]
        second_subsequence = time_series[second_start_index:second_start_index + candidate_length]

        candidate_distance = self._calculate_scale_aware_distance(first_subsequence, second_subsequence)

        if candidate_distance > self.distance_threshold:
            return None

        motif_candidate = MotifCandidate(
            first_start_index=first_start_index,
            second_start_index=second_start_index,
            length=candidate_length,
            diagonal_shift=diagonal_shift,
            distance=candidate_distance,
            event_count=len(event_group)
        )

        return motif_candidate

    def _calculate_scale_aware_distance(self, first_subsequence: np.ndarray, second_subsequence: np.ndarray) -> float:
        if first_subsequence.shape != second_subsequence.shape:
            raise ValueError("Subsequences must have the same shape.")

        first_normalized = self._z_normalize(first_subsequence)
        second_normalized = self._z_normalize(second_subsequence)

        difference_values = first_normalized - second_normalized
        raw_shape_distance = np.sqrt(np.sum(difference_values ** 2))

        time_steps = first_subsequence.shape[0]
        feature_count = first_subsequence.shape[1]
        normalized_shape_distance = raw_shape_distance / (2.0 * np.sqrt(time_steps * feature_count))

        first_scale = self._calculate_global_scale(first_subsequence)
        second_scale = self._calculate_global_scale(second_subsequence)
        scale_distance = self._calculate_single_scale_distance(first_scale, second_scale)

        final_distance = np.sqrt(normalized_shape_distance ** 2 + scale_distance ** 2) / np.sqrt(2.0)
        return float(final_distance)

    def _z_normalize(self, subsequence: np.ndarray) -> np.ndarray:
        mean_values = np.mean(subsequence, axis=0)
        standard_deviation_values = np.std(subsequence, axis=0)

        safe_standard_deviation_values = standard_deviation_values.copy()
        safe_standard_deviation_values[safe_standard_deviation_values < 1e-12] = 1.0

        normalized_subsequence = (subsequence - mean_values) / safe_standard_deviation_values
        return normalized_subsequence

    def _calculate_global_scale(self, subsequence: np.ndarray) -> float:
        standard_deviation_values = np.std(subsequence, axis=0)
        global_scale = np.sqrt(np.mean(standard_deviation_values ** 2))
        return float(global_scale)

    def _calculate_single_scale_distance(self, first_scale: float, second_scale: float) -> float:
        smaller_scale = min(first_scale, second_scale)
        larger_scale = max(first_scale, second_scale)

        if smaller_scale < 1e-12:
            raw_scale_distance = 0.0
        else:
            raw_scale_distance = larger_scale / smaller_scale - 1.0

        capped_scale_distance = min(raw_scale_distance, self.scale_cap) / self.scale_cap
        return float(capped_scale_distance)

    def _remove_overlapping_candidates(self, motif_candidates: list[MotifCandidate]) -> list[MotifCandidate]:
        selected_candidates = []
        used_ranges = []

        for motif_candidate in motif_candidates:
            first_range = (motif_candidate.first_start_index,
                           motif_candidate.first_start_index + motif_candidate.length)
            second_range = (motif_candidate.second_start_index,
                            motif_candidate.second_start_index + motif_candidate.length)

            if self._range_overlaps_any_used_range(first_range, used_ranges):
                continue

            if self._range_overlaps_any_used_range(second_range, used_ranges):
                continue

            selected_candidates.append(motif_candidate)
            used_ranges.append(first_range)
            used_ranges.append(second_range)

        return selected_candidates

    def _range_overlaps_any_used_range(self, candidate_range: tuple[int, int],
                                       used_ranges: list[tuple[int, int]]) -> bool:
        for used_range in used_ranges:
            if self._ranges_overlap(candidate_range, used_range):
                return True

        return False

    def _ranges_overlap(self, first_range: tuple[int, int], second_range: tuple[int, int]) -> bool:
        first_start, first_end = first_range
        second_start, second_end = second_range

        if first_start < second_end and second_start < first_end:
            return True

        return False