from enum import Enum
import numpy as np
from anomrank.graph import Node


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
    graph : Graph
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
    num_nodes = len(graph._nodes)
    # Initialize the output array
    scores = np.empty(num_nodes)

    if version == Version.V1:
        for i in range(num_nodes):
            scores[i] = CONSTANT / num_nodes
    else:
        for i in range(num_nodes):
            scores[i] = CONSTANT * graph._nodes[i].total_weight / num_edges

    prev_scores = np.copy(scores)
    score_delta = 100

    while score_delta > EPSILON:
        new_scores = np.zeros(num_nodes)

        for i in range(num_nodes):
            if prev_scores[i] == 0:
                continue
            node = graph._nodes[i]
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
            scores[i] += new_scores[i]

        score_delta += np.sum(np.absolute(new_scores[i]))

        prev_scores = new_scores

    # Normalize the output scores
    scores /= np.sum(scores)

    return scores
