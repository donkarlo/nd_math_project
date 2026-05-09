import numpy as np

from nd_sociomind.experiment.parts.oldest.uav1_300k_normal_time_position_modality import \
    Uav1300kNormalTimePositionModality
from period_limited_variable_length_motif_discoverer import PeriodLimitedVariableLengthMotifDiscoverer


class GpsMotifTest:
    def __init__(self):
        self.time_positions_composite_memory = None

    def run(self) -> None:
        gps_time_series = self._load_gps()

        print(f"GPS time series shape: {gps_time_series.shape}")
        print(f"First point: {gps_time_series[0]}")
        print(f"Last point: {gps_time_series[-1]}")

        discoverer = PeriodLimitedVariableLengthMotifDiscoverer(
            window_size=80,
            distance_threshold=0.15,
            minimum_shift=24000,
            maximum_shift=24900,
            shift_step=5,
            scale_cap=4.0,
            max_event_gap=10,
            minimum_event_count=8,
            maximum_motifs=20
        )

        motifs = discoverer.discover(gps_time_series)

        print("==========")
        print(f"Detected motifs: {len(motifs)}")

        for motif_index, motif in enumerate(motifs):
            print("-----")
            print(f"Motif index: {motif_index}")
            print(motif.to_text())

    def _load_gps(self) -> np.ndarray:
        data_slice = slice(0, 50000)
        self.time_positions_composite_memory = Uav1300kNormalTimePositionModality(data_slice)
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


if __name__ == "__main__":
    test = GpsMotifTest()
    test.run()