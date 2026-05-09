class MotifCandidate:
    def __init__(self, first_start_index: int, second_start_index: int, length: int, diagonal_shift: int,
                 distance: float, event_count: int):
        self.first_start_index = first_start_index
        self.second_start_index = second_start_index
        self.length = length
        self.diagonal_shift = diagonal_shift
        self.distance = distance
        self.event_count = event_count

    def get_occurrence_start_indices(self) -> list[int]:
        return [self.first_start_index, self.second_start_index]

    def to_text(self) -> str:
        lines = [
            f"First start index: {self.first_start_index}",
            f"Second start index: {self.second_start_index}",
            f"Length: {self.length}",
            f"Diagonal shift: {self.diagonal_shift}",
            f"Distance: {self.distance}",
            f"Event count: {self.event_count}",
            f"Occurrences: {self.get_occurrence_start_indices()}"
        ]

        return "\n".join(lines)