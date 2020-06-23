from anomrank.anomaly_detect import compute_first_derivative, compute_second_derivative


def test_first_derivative():
    t1 = 5
    t2 = 3

    result = compute_first_derivative(t1, t2)
    expected = -2

    assert expected == result


def test_second_derivative():
    t1 = 3
    t2 = 1
    t3 = -1

    result = compute_second_derivative(t1, t2, t3)
    expected = 0

    assert expected == result
