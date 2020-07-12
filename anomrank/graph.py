import numpy as np


class Node:
    "A node in the network graph."

    def __init__(self):
        self._total_weight = 0
        self._out_edges = []
        self._weights = []

    @property
    def total_weight(self):
        "Returns the sum of all the weights of this node's edges."
        return self._total_weight

    @property
    def edges(self):
        """Returns an iterator of pairs, each consisting of an edge and
        its corresponding weight.
        """
        return zip(self._out_edges, self._weights)

    @property
    def edge_count(self):
        "Returns the number of edges going out from this node."
        return len(self._out_edges)

    def add_edge(self, target, weight):
        """Adds an edge from this node to another one.

        If the edge already exists, the method simply adds the weight to it.

        Parameters
        ----------
        target : int
            The destination node's label
        weight : int
            Weight to add to this edge
        """
        # Update the cached total weight
        self._total_weight += weight

        # See if we already had an edge to this node
        try:
            index = self._out_edges.index(target)
            # Add the weight to the existing edge
            self._weights[index] += weight
        except ValueError:
            # Create a new edge
            self._out_edges.append(target)
            self._weights.append(weight)


class Graph:
    """ A graph that holds the Nodes.

    To hold the data it uses an adjaceny list.

    """

    def __init__(self):
        self._nodes = []

    def print_nodes(self):
        "Shows all the Nodes in the graph."
        print(self._nodes)

    def add_node(self, node):
        "Adds the Node to the current Graph."
        self._nodes.append(node)

    def inject_snapshot(self, inject_num, init_ss, test_num, snapshots, inject_ss):

        for _ in range(inject_num):
            injected = init_ss + np.random.random_integers(test_num)

            while injected not in inject_ss:
                injected = init_ss + np.random.random_integers(test_num)

            inject_ss.append(injected)

            if injected in snapshots:
                snapshots.append(injected)

        snapshots.sort()
        inject_ss.sort()

        return snapshots, inject_ss
