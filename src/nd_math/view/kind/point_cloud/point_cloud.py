from nd_math.view.view import View
from nd_math.view.kind.point_cloud.point.group.group import Group as PointGroup
import numpy as np
from typing import Union

class PointCloud(View):
    def __init__(self, point_group: PointGroup) -> None:

        View.__init__(self, point_group)

    def _build(self) -> None:
        self.get_axis().scatter(*self.get_point_group().get_members().T, s=1)
