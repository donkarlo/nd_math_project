from abc import ABC, abstractmethod
from typing import Protocol


class Interface(ABC, Protocol):
    @abstractmethod
    def render(self)->None:
        pass