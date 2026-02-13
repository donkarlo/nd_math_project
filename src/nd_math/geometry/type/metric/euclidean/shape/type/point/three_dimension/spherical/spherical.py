from nd_math.geometry.type.metric.euclidean.shape.type.point.two_dimension.polar import Polar


class Spherical(Polar):
    def __init__(self, radius, xy_angle: float, xy_z_angle: float):
        super().__init__(radius, xy_angle)
        self._radius = radius
        self._xy_angle = xy_angle
        self._xy_z_angle = xy_z_angle

    def get_radius(self)->float:
        return self._radius

    def get_xy_angle(self) -> float:
        return self._xy_angle

    def get_xy_z_angle(self) -> float:
        return self._xy_z_angle
