from abc import ABC, abstractmethod
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Union

from nd_math.view.kind.point_cloud.point.group.group import Group


class Interface(ABC):

    @abstractmethod
    def _build(self) -> None: ...

    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def get_dimension(self) -> int: ...

    @abstractmethod
    def get_axis(self) -> Union[Axes, Axes3D]: ...

    @abstractmethod
    def get_figure(self) -> Figure: ...

    @abstractmethod
    def get_point_group(self)->Group: ...