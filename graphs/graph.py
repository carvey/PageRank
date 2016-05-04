import pandas as pd
import numpy as np

from orderedset import OrderedSet
from collections import OrderedDict

from .node import Node

pd.set_option('display.width', 100)

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
        for equality in order to find the desired node

        :param name: the name of the node to search for
        :return: the node with `name` if it is present in the graphs node_set
        """
        target_node = Node(name)

        if target_node in self.node_set:
            for node in self.node_set:
                if node == target_node:
                    return node

        return None

    def create_h_matrix(self, df=None, store=True):
        """
        Adjacency matrix
        :return:
        """
        # set up default matrix (n x n with all 0 values)
        if not df:
            df = self.h_matrix

        df = self.dataframe_nxn()

        for node in self.node_set:
            adjacency_map = node.compute_adjacency()

            for adjacent_node, probability in adjacency_map.items():
                df.set_value(node, adjacent_node, probability)

        if store:
            self.h_matrix = df

        return df


    def create_s_matrix(self, df=None, store=True):
        """
        Transition Stochastic Matrix
        :return:
        """
        if not df:
            df = self.create_h_matrix(store=False)

        def correct_dangling(row):
            if row.sum() == 0:
                return [1/len(row) for node in self.node_set]

            else:
                return row

        df = df.apply(correct_dangling, axis=1, reduce=False)


        if store:
            self.s_matrix = df

        return df


    def create_g_matrix(self, df=None, store=False):
        """
        Google Matrix
        :return:
        """
        scaling_param = .9
        if not df:
            df = self.create_s_matrix(store=False)

        df = np.dot(.9, df)
        df += np.dot((1-scaling_param), 1/len(self.node_set))

        return df

    def compute_page_rank(self, df=None):
        if not df:
            df = self.create_g_matrix()

        vector = [1/len(self.node_set) for x in self.node_set]

        for node in self.node_set:
            vector = np.dot(vector, df)

        vector = vector.round(3)
        page_map = {}
        for i, node in enumerate(self.node_set):
            page_map[node] = vector[i]

        return page_map


    def describe_graph(self):
        print("Details for graph: %s" % self.name)
        print("++++ Nodes in the graph")
        for node in self.node_set:
            print("NodeName = %s" % node.name)

        print("++++ Edges in the Graph")
        for node in self.node_set:
            node.describe()

        print("\n\nAdjency Matrix:\n")
        print(self.create_h_matrix().round(3))

        print("\n\nTransition Stochastic Matrix:\n")
        print(self.create_s_matrix().round(3))

        print("\n\nGoogle Matrix:\n")
        print(self.create_g_matrix().round(3))

        print("\n\nRankings:\n")

        data = self.compute_page_rank()

        sorted_nodes = sorted(data, key=data.get, reverse=True)
        for i, node in enumerate(sorted_nodes):
            print("Rank #%s: %s - %s" % (i+1, node, data[node]))


    def dataframe_nxn(self):
        structure = OrderedDict()
        blank_data = [0.0 for node in self.node_set]

        for node in self.node_set:
            structure[node] = pd.Series(blank_data, index=self.node_set)

        return pd.DataFrame(structure)