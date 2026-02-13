from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.axes import Axes
from typing import Union
from matplotlib.figure import Figure
from types import ModuleType
import numpy as np

from nd_math.view.interface import Interface
from nd_math.view.kind.point_cloud.point.group.group import Group as PointGroup


class View(Interface, ABC):
    def __init__(self, point_group: PointGroup):
        self._point_group = point_group
        pair_set_members = np.asarray(self._point_group.get_members())
        #TODO for the moment from here it is nd array
        if pair_set_members.ndim != 2 or pair_set_members.shape[1] not in (2, 3):
            raise ValueError("group must be a 2D array with shape (n, 2) or (n, 3)")

        self._dimension = None
        self._pyplot_figure = plt.figure()
        if pair_set_members.shape[1] == 2:
            self._pyplot_axis = self._pyplot_figure.add_subplot(111)
            self._dimension = 2
        elif pair_set_members.shape[1] == 3:
            self._pyplot_axis = self._pyplot_figure.add_subplot(111, projection='3d')
            self._dimension = 3

    def get_point_group(self) -> PointGroup:
        return self._point_group

    def get_axis(self) -> Union[Axes, Axes3D]:
        return self._pyplot_axis

    def get_figure(self) -> Figure:
        return self._pyplot_figure

    def get_pyplot(self)-> ModuleType:
        return plt

    def get_dimension(self) -> int:
        return self._dimension

    def get_point_group(self):
        return self._point_group

    def render(self):
        self._build()
        self.get_pyplot().show()
