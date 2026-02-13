from dataclasses import dataclass

from nd_utility.data.kind.graphic.color.color import Color


class Style:
    def __init__(self, color:Color, size:int):
        self._color = color

    def get_keyword_arguments(self) -> dict:
        return {"color": self._color}