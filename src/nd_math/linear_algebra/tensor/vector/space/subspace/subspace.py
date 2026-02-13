from abc import ABC, abstractmethod

class Subspace(ABC):
    def __init__(self, dimension:int):
        self._dimension = dimension

    @abstractmethod
    def validate_zero_existance(self)->bool:
        pass

    @abstractmethod
    def validdate_closed_to_summation(self)->bool:
        pass

    @abstractmethod
    def velidate_closed_to_scalar_multiplication(self)->bool:
        pass