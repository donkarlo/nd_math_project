from nd_math.geometry.type.metric.euclidean.shape.shape import Shape
from nd_math.linear_algebra.tensor.vector.vector import Vector
from nd_math.linear_algebra.tensor.vector.vector_representable import VectorRepresentable


class Point(Shape, VectorRepresentable):
    """
    A point is not a vector, it can be represented as a vector.
    """
    def __init__(self, coordinates: List[float]):
        self._coordinates = coordinates

        self._vec_representation = None

    def get_vector_representation(self):
        self._vec_representation = Vector(self._coordinates)
        return self._vec_representation
