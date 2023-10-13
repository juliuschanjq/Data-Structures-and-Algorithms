class Graph:
    def __init__(self, gdict=None):
        if gdict is None:
            gdict = {}
        self.gdict = gdict

    def edges(self):
        return self.find_edges()

    # Add the new edge
    def add_edge(self, edge):
        edge = set(edge)
        (vrtx1, vrtx2) = tuple(edge)
        if vrtx1 in self.gdict:
            self.gdict[vrtx1].append(vrtx2)
        else:
            self.gdict[vrtx1] = [vrtx2]

    # List the edge names
    def find_edges(self):
        edge_names = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if {nxtvrtx, vrtx} not in edge_names:
                    edge_names.append({vrtx, nxtvrtx})
        return edge_names

# Create the dictionary with graph elements
graph_elements = {
    "a": ["b", "c"],
    "b": ["a", "d"],
    "c": ["a", "d"],
    "d": ["e"],
    "e": ["d"]
}

g = Graph(graph_elements)
g.add_edge({'a', 'e'})
g.add_edge({'a', 'c'})
print(g.edges())
