import pandas as pd

from .edge import Edge


class Node:

    def __init__(self, name):
        self.name = name
        self.edges = set()

    def __eq__(self, other):

        try:
            if self.name == other.name:
                return True
        except:
            return False

        return False

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def add_edge(self, target_node):
        edge = Edge(self, target_node)
        self.edges.add(edge)

    def describe(self):
        for edge in self.edges:
            edge.describe()

    def compute_adjacency(self):
        adjacency_map = {}

        if self.edges:
            probability = 1 / len(self.edges)

            for edge in self.edges:
                adjacency_map[edge.target_node] = probability

        return adjacency_map
