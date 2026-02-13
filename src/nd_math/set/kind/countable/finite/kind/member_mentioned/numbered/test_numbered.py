from nd_math.set.kind.countable.finite.kind.member_mentioned.numbered.numbered import Numbered
import numpy as np

class TestNumbered:
    def setup_method(self):
        self._three_d_np_numbered_set = Numbered(np.array([
            [1, 2, 0],
            [2, 1, 1],
            [3, 2, 1],
            [4, 1, 2],
            [5, 3, 2],
            [6, 2, 3],
            [7, 3, 3],
            [8, 4, 4],
            [9, 5, 4],
            [10, 4, 5],
            [11, 6, 5],
            [12, 5, 6],
            [13, 7, 6],
            [14, 6, 7],
            [15, 8, 7],
            [16, 7, 8],
            [17, 9, 8],
            [18, 8, 9],
            [19, 10, 9],
            [20, 9, 10],
        ]))



    def test_is_member(self):
        assert self._three_d_np_numbered_set.is_member(np.array([8, 4, 4]))
        assert not self._three_d_np_numbered_set.is_member(np.array([8, 6, 4]))

