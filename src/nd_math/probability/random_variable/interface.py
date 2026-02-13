from nd_math.probability.sample_space.sample_space import SampleSpace
from typing import Protocol
from abc import ABC, abstractmethod


class Interface(Protocol):
    _sample_space: SampleSpace

    @abstractmethod
    def get_value(self, x) -> float: ...
