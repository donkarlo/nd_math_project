from nd_math.number.type_hint.type_hint import ScalarType

class CloseUnitIntervalNumber:
    def __init__(self, value: ScalarType):
        self._value = value
        if value <= 0 or value >= 1:
            raise ValueError("The value is not between 0 and 1")

    def get_value(self) -> ScalarType:
        return self._value
