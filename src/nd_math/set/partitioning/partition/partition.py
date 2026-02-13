from nd_math.set.set import Set
from typing import List, Any


class Partition(Set):
    def __init__(self, partions: List[Set]):
        Set.__init__(self, partions)

    def get_partitions(self) -> List[Set]:
        return self._members

    def is_member(self, member: Any) -> bool:
        if member in self.get_members():
            return True
        return False


