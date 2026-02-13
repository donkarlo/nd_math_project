from nd_math.graph.edge.edge import Edge
from typing import Protocol, List


class Interface(Protocol):
    _vertices: List[Vertex]
    _edges: List[Edge]
