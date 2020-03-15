from itertools import islice
from typing import NamedTuple


class TimeEdge(NamedTuple):
    """Stores an edge in the dynamic edge, together with its timestamp.

    It's important for the edges to be sorted correctly by their timestamp,
    therefore please keep the `time` field first.
    """
    time: int
    source: int
    target: int
    is_attack: bool


def read_data(path, step_size, max_lines=None):
    """Reads network flow data from a file.

    Parameters
    ----------
    path : str
        The path of the text file to read from.
    step_size : int
        Distance between two consecutive timestamps choosen as snapshots.
    max_lines : int, optional
        Up to how many lines to read from the input file.
        If `None` (the default), reads the whole file.

    Returns
    -------
    num_timestamps : int
        How many distinct timestamps were found in the input.
    num_nodes : int
        How many distinct network nodes were found in the input.
    edges : list of `TimeEdge`
        All the packets that were sent in the network,
        ordered by their timestamp.
    snapshots : list of `int`
        Timestamps at which to analyse network traffic.
    """
    edges = []
    with open(path) as fin:
        for line in islice(fin, max_lines):
            time, source, target, is_attack = map(int, line.split())

            edge = TimeEdge(time, source, target, bool(is_attack))
            edges.append(edge)

    initial_time = min(map(lambda ed: ed.time, edges))
    end_time = max(map(lambda ed: ed.time, edges))
    num_timestamps = end_time - initial_time + 1

    initial_node = min(map(lambda ed: min(ed.source, ed.target), edges))
    end_node = max(map(lambda ed: max(ed.source, ed.target), edges))
    num_nodes = end_node - initial_node + 1

    # Subtract the starting time and the index of the starting node to make the
    # counters start at 0.
    edges = [
        TimeEdge(edge.time - initial_time, edge.source - initial_node,
                 edge.target - initial_node, edge.is_attack)
        for edge in edges
    ]

    # Sort the edges by their timestamps ascending
    edges.sort()

    snapshots = []
    step = 1
    for edge in edges:
        if step * step_size < edge.time:
            snapshots.append(step)
            step = edge.time // step_size + 1

    # Make sure the step after the last edge is added,
    # if it's not already there
    if snapshots and step != snapshots[-1]:
        snapshots.append(step)

    return num_timestamps, num_nodes, edges, snapshots
