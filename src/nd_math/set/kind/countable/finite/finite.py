from abc import abstractmethod

from nd_math.set.kind.countable.countable import Countable
from typing import Any, List

class Finite(Countable):
    def __init__(self, members:Any):
        Countable.__init__(self, members)

    @abstractmethod
    def get_all_subsets(self)->List["Finite"]:
        pass

