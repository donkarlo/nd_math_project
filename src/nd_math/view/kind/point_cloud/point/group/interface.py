from abc import ABC, abstractmethod
from typing import Dict

class Interface(ABC):
    @abstractmethod
    def get_keyword_arguments(self)->Dict:
        pass
