from nd_math.graph.vertex import Vertex


class Edge:
    def __init__(self, vertex1: Vertex, vertex2: Vertex):
        self._vertex1 = vertex1
        self._vertex2 = vertex2
