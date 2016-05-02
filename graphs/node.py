from .edge import Edge


class Node:

    def __init__(self, name):
        self.name = name
        self.edges = set()

    def __eq__(self, other):
        if self.name == other.name:
            return True

        return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def add_edge(self, target_node):
        edge = Edge(self, target_node)
        self.edges.add(edge)

    def describe(self):
        for edge in self.edges:
            edge.describe()
