from orderedset import OrderedSet

from .node import Node
from .edge import Edge

class Graph:

    def __init__(self, name):
        self.name = name
        self.node_set = OrderedSet()
        self.edge_set = OrderedSet()

        self.h_matrix = None
        self.s_matrix = None
        self.g_matrix = None
        self.pi_vector = None

    def create_graph_from_file(self, file):
        for line in file.read().splitlines():

            if "NodeName" in line:
                node_name = line.split(" = ")[1]
                node = Node(node_name)

                self.node_set.add(node)

            if "EdgeName" in line:
                nodes = line.split(" = ")[1].split("->")
                starting_node_name = nodes[0]
                target_node_name= nodes[1]

                starting_node = self.find_node(starting_node_name)
                target_node = self.find_node(target_node_name)

                if starting_node is None or target_node is None:
                    raise RuntimeError

                starting_node.add_edge(target_node)

    def find_node(self, name):
        """
        Since sets do not support getting an item out, loop over and compare each node
        for equality

        :param name: the name of the node to search for
        :return: the node with `name` if it is present in the graphs node_set
        """
        target_node = Node(name)

        if target_node in self.node_set:
            for node in self.node_set:
                if node == target_node:
                    return node

        return None

    def create_h_matrix(self):
        pass

    def create_s_matrix(self):
        pass

    def create_g_matrix(self):
        pass

    def compute_page_rank(self):
        pass

    def describe_graph(self):
        print("++++ Nodes in the graph")
        for node in self.node_set:
            print("NodeName = %s" % node.name)

        print("++++ Edges in the Graph")
        for node in self.node_set:
            node.describe()

    def describe_matrix(self):
        pass

