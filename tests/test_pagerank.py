from anomrank.pagerank import EPSILON, Version, pagerank
from anomrank.graph import Node, Graph
import numpy as np


def create_graph():
    "Creates a simple, fully connected graph"

    g = Graph()

    a = Node()
    a.add_edge(1, 5)
    a.add_edge(2, 3)
    b = Node()
    b.add_edge(2, 1)
    c = Node()
    c.add_edge(0, 7)

    g.add_node(a)
    g.add_node(b)
    g.add_node(c)

    return g


def test_pagerank_v1():
    graph = create_graph()
    num_edges = graph.num_edges
    scores = pagerank(graph, num_edges, Version.V1)
    expected = np.array([0.3589, 0.2564, 0.3846])
    np.testing.assert_allclose(scores, expected, rtol=EPSILON)


def test_pagerank_v2():
    graph = create_graph()
    num_edges = graph.num_edges
    scores = pagerank(graph, num_edges, Version.V2)
    expected = np.array([0.4434, 0.1697, 0.3867])
    np.testing.assert_allclose(scores, expected, rtol=EPSILON)
