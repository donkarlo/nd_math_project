from nd_math.graph.graph import Graph


class Tree(Graph):
    def __init__(self, vertices: List[Vertex], edges: List[Edge]):
        super().__init__(vertices, edges)
