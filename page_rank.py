from graphs.graph import Graph

data = open("graph_data/PageRank_03.txt")
graph = Graph("Page Rank Data 03")
graph.create_graph_from_file(data)

graph.describe_graph()