class Size:
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Size value must be an integer")
        self._value = value

    def get_value(self) -> int:
        return self._value
