from typing import Any
from abc import ABC, abstractmethod

class Set(ABC):
    """

    """
    def __init__(self, members:Any):
        """
        Members can be defined of names, objects and even in numbers they can be defined as continous intervals so we can just write members
        Args:
            members:
        """
        self._members = members


    def get_members(self)->Any:
        return self._members

    @abstractmethod
    def is_member(self, member:Any) -> bool:
        pass