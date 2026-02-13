from nd_math.geometry.type.metric.euclidean.shape.three_d import ThreeD
from physix.dimension.unit import Unit


class HollowNestedCubes(ThreeD):
    def __init__(self, height: float, thickness: float, inner_side_length: float, outer_side_length: float, unit: Unit):
        self._height = height
        self._thickness = thickness
        self._inner_side_length = inner_side_length
        self._outer_side_length = outer_side_length
        self._unit = unit
