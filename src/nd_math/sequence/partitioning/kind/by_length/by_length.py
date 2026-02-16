import numpy as np


class ByLength:
    def __init__(self, sequence: np.ndarray, length: int):
        self._length = length
        self._sequence = sequence

    def get_full_length_partitions(self) -> np.ndarray:

        usable_len = (len(self._sequence) // self._length) * self._length
        usable_partitions_sequence = self._sequence[:usable_len]
        partition_count = len(usable_partitions_sequence) // self._length

        self._partitions = usable_partitions_sequence.reshape(partition_count, self._length,
                                                              usable_partitions_sequence.shape[1])

        return self._partitions
