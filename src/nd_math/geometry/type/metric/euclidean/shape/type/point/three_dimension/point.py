from typing import List

from nd_math.linear_algebra.tensor.vector.vector_representable import VectorRepresentable
from nd_math.geometry.type.metric.euclidean.shape.type.point.point import Point as BasePoint


class Point(BasePoint, VectorRepresentable):
    def __init__(self, coordinates:List[float]):
        if len(coordinates) != 3:
            raise ValueError("value of coordinates must be 3")
        super().__init__(coordinates)