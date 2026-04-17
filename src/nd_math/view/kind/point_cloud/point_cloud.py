import numpy as np

from nd_math.view.kind.point_cloud.point.group.group import Group as PointGroup
from nd_math.view.view import View


class PointCloud(View):
    def __init__(self, point_group: PointGroup) -> None:
        View.__init__(self, point_group)

    def _build(self) -> None:
        np_members = np.asarray(self.get_point_group().get_members())
        self.get_axis().scatter(*np_members.T, s=1)
