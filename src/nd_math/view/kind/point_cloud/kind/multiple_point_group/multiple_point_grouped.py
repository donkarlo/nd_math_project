from nd_math.view.kind.point_cloud.point.group.group import Group as PointGroup
from typing import List

from nd_math.view.kind.point_cloud.point_cloud import PointCloud


class MultiplePointGrouped(PointCloud):
    def __init__(self, multiple_point_group= List[PointGroup]):
        self._multiple_point_group = multiple_point_group

    def get_multiple_point_group(self)-> PointGroup:
        return self._multiple_point_group

    def _build(self)->None:
        for point_group in self._multiple_point_group:
            self._point_group = point_group
            PointCloud._build(self)
