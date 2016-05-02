
class Edge:

    def __init__(self, starting_node, target_node):
        self.starting_node = starting_node
        self.target_node = target_node

    def describe(self):
        serialized = "%s -> %s" % (self.starting_node, self.target_node)
        print("EdgeName = %s" % serialized)
