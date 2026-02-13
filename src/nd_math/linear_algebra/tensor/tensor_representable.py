from typing import Protocol, TYPE_CHECKING, runtime_checkable

if TYPE_CHECKING:
    from nd_math.linear_algebra.tensor.tensor import Tensor

@runtime_checkable
class TensorRepresentable(Protocol):
    def get_tensor_representation(self) -> "Tensor": ...