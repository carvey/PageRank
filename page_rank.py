from graphs.graph import Graph

data = open("graph_data/PageRank_03.txt")
graph = Graph("PageRank_03.txt")
graph.create_graph_from_file(data)

print(
"""
CSCI 5330 Spring 2016
Charles Arvey
900815172
""")
graph.describe_graph()