from typing import Any

from nd_math.set.partitioning.partition.partition import Partition
from nd_math.set.set import Set


class SubsetComplement(Partition):
    def __init__(self, subset: Set, complement: Set):
        self._subset = subset
        self._complement = complement

    def get_complement(self):
        return self._complement

    def get_subset(self):
        return self._subset

    def get_universal_set(self)->Set:
        pass

    def is_member(self, member: Any) -> bool:
        if member in self.get_members():
            return True
        return False


