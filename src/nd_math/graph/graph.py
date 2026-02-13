from nd_math.graph.edge.edge import Edge
from nd_math.graph.vertex import Vertex
from typing import List


class Graph:
    def __init__(self, vertices: List[Vertex], edges: List[Edge]):
        self._vertices = vertices
        self._edges = edges
