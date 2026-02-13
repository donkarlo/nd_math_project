from typing import List

import numpy as np

from nd_math.number.type_hint.type_hint import TensorType
from nd_math.set.kind.countable.finite.finite import Finite
from nd_math.set.kind.countable.finite.kind.member_mentioned.members_mentioned import MembersMentioned


class Numbered(MembersMentioned):
    def __init__(self, members: np.ndarray):
        if not isinstance(members, np.ndarray):
            raise TypeError("members must be a numpy array")

        MembersMentioned.__init__(self, members)

    def get_all_subsets(self) -> List["Finite"]:
        return []

    def is_member(self, member: TensorType) -> bool:
        # scalar case
        if isinstance(member, (int, float)):
            return member in self._members

        # list / tuple -> convert to ndarray
        if isinstance(member, (list, tuple)):
            member = np.array(member)

        # ndarray case
        if isinstance(member, np.ndarray):
            # must be 1D and compatible with member dimension
            if member.ndim != 1:
                return False
            if member.shape[0] != self._members.shape[1]:
                return False

            return np.any(np.all(self._members == member, axis=1))
        return False
    def get_size(self) -> int:
        return self._members.shape[0]