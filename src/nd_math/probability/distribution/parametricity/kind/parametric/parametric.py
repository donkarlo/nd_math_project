from typing import Tuple

from nd_utility.data.kind.group.group import Group


class Parametric:
    def __init__(self, parameters: Tuple):
        """
        Number of the parameters of a parametric distribution is contant
        Args:
            parameters:
        """
        self._parameters = parameters

    def get_parameters(self) -> Tuple:
        return self._parameters
