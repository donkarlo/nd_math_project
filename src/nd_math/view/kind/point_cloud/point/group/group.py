from typing import Union, List

import numpy as np

from nd_utility.data.kind.group.group import Group as BaseGroup


class Group(BaseGroup):
    def __init__(self, members: np.ndarray):
        BaseGroup.__init__(self, members)

    def get_column_by_index(self, index: int) -> np.ndarray:
        return self.get_members()[:index]
