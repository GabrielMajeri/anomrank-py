from anomrank.read_data import read_data


def test_read_data():
    path = "tests/data.txt"
    step_size = 3

    num_timestamps, num_nodes, edges, snapshots = read_data(path, step_size)

    assert 22 == num_timestamps
    assert 9 == num_nodes
    assert 11 == len(edges)
    assert 0 == edges[0].source
    assert 3 == len(snapshots)
    assert 3 == snapshots[1]


def test_read_data_with_max_lines():
    path = "tests/data.txt"
    step_size = 3
    max_lines = 4

    _, _, edges, _ = read_data(path, step_size, max_lines)

    assert max_lines == len(edges)
