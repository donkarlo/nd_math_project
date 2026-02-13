from typing import Protocol


class System(Protocol):
    def change_origin(self, new_origin:List[float]): ...
    def change_point_system(self, point:Point, new_system:System): ...


