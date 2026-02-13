from nd_math.plot.kind.scatter.decorator.decorator import Decorator
from nd_math.plot.kind.scatter.interface import Interface
import numpy as np
from typing import List
from nd_math.view.kind.decorator.multi_data_set import MultiDataSet


class PairLineConnected(Decorator):
    def __init__(self, inner:MultiDataSet, datas:List[np.nd_array]):
        Decorator.__init__(self, inner, datas)