class Animation:
    def __init__(self, speed:float):
        self._speed = speed

    def get_speed(self)->float:
        return self._speed