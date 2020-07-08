from enum import Enum
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


class Version(Enum):
    "Version of the PageRank algorithm to use"
    V1 = 1
    V2 = 2


# Constant factor for the initial probability distribution
# - For the first version, all the scores are initialized to
#   CONSTANT / (number of nodes)
# - For the second version, all the scores are initialized to
#   CONSTANT * (total weight of outgoing edges) / (number of edges)
CONSTANT = 0.5

# When the difference between two consecutive PageRank score vectors becomes
# less than this, we assume the algorithm converged.
EPSILON = 1e-3


def pagerank(graph, num_edges, version):
    """ Computes the PageRank scores for a network graph.

    Parameters
    ----------
    graph : list of `Node`
        Graph for which to compute the PageRank.
    num_edges : int
        Number of edges in the graph.
    version : Version
        Which version of the algorithm to use

    Returns
    -------
    numpy array of PageRank scores
    """
    assert isinstance(version, Version)
    num_nodes = len(graph)
    # Initialize the output array
    scores = np.empty(num_nodes)

    if version == Version.V1:
        for i in range(num_nodes):
            scores[i] = CONSTANT / num_nodes
    else:
        for i in range(num_nodes):
            scores[i] = CONSTANT * graph[i].total_weight / num_edges

    prev_scores = np.copy(scores)
    score_delta = 100

    while score_delta > EPSILON:
        new_scores = np.zeros(num_nodes)

        for i in range(num_nodes):
            if prev_scores[i] == 0:
                continue
            node = graph[i]
            if node.total_weight == 0:
                continue

            if version == Version.V1:
                delta = (1 - CONSTANT) * prev_scores[i] / node.edge_count
                for neighbor, _ in node.edges:
                    new_scores[neighbor] += delta
            else:
                delta = (1 - CONSTANT) * prev_scores[i] / node.total_weight
                for neighbor, weight in node.edges:
                    new_scores[neighbor] += delta * weight

        score_delta = 0
        for i in range(num_nodes):
            score_delta += abs(new_scores[i])
            scores[i] += new_scores[i]

        prev_scores = new_scores

    # Normalize the output scores
    scores /= np.sum(scores)

    return scores
