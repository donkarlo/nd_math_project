from nd_math.plot.plot import Plot
import numpy as np

from nd_math.plot.style.style import Style


class TwoDimension(Plot):
    def __init__(self, pairs:np.ndarray, styles:Style):
        Plot.__init__(self, pairs, styles)
        self._component_one_column = pairs[:, 0]
        self._component_two_column = pairs[:, 1]

    def get_component_one_column(self)->np.ndarray:
        return self._component_one_column

    def get_component_two_column(self)->np.ndarray:
        return self._component_two_column