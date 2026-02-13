from nd_math.linear_algebra.tensor.tensor import Tensor
from typing import Union

class Scalar(Tensor):
    def __init__(self, value:Union[int,float]):
        self._value = value
    def get_value(self):
        pass
