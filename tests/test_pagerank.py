from anomrank.pagerank import EPSILON, Node, Version, pagerank
import numpy as np


def create_graph():
    "Creates a simple, fully connected graph"
    a = Node()
    a.add_edge(1, 5)
    a.add_edge(2, 3)
    b = Node()
    b.add_edge(2, 1)
    c = Node()
    c.add_edge(0, 7)

    return [a, b, c]


def count_edges(graph):
    "Counts the total number of edges in a graph"
    num = 0
    for node in graph:
        num += node.edge_count
    return num


def test_pagerank_v1():
    graph = create_graph()
    num_edges = count_edges(graph)
    scores = pagerank(graph, num_edges, Version.V1)
    expected = np.array([0.3589, 0.2564, 0.3846])
    np.testing.assert_allclose(scores, expected, rtol=EPSILON)


def test_pagerank_v2():
    graph = create_graph()
    num_edges = count_edges(graph)
    scores = pagerank(graph, num_edges, Version.V2)
    expected = np.array([0.4434, 0.1697, 0.3867])
    np.testing.assert_allclose(scores, expected, rtol=EPSILON)
