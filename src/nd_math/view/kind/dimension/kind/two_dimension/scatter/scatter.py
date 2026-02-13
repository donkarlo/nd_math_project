from nd_math.plot.plot import Plot
import numpy as np
import matplotlib.pyplot as plt

from nd_math.plot.kind.scatter.style.style import Style


class Scatter(Plot):
    def __init__(self, pairs:np.ndarray, styles:Style):
        Plot.__init__(self, pairs, styles)
        plt.scatter(pairs[:, 0], pairs[:, 1])

    def add_plot(self, pairs:np.ndarray, style:Style)->None:
        plt.scatter(pairs[:, 0], pairs[:, 1])

    def show(self)->None:
        plt.show()
