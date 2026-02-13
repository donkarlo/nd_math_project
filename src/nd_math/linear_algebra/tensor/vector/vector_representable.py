from nd_math.linear_algebra.tensor.tensor_representable import TensorRepresentable
from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from nd_math.linear_algebra.tensor.vector.vector import Vector


@runtime_checkable
class VectorRepresentable(TensorRepresentable, Protocol):
    """
    For things whic are reppresentable by vector
    """
    _vector_representation: "Vector"
    def get_vector_representation(self)-> "Vector": ...