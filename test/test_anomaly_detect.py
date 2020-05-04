import pytest
import numpy as np
import random
from anomrank.anomaly_detect import normalize_online


def test_normalize_online_function_1():
    timestamp = 1
    delta = np.zeros(4)
    mean = np.zeros(4)
    var = np.zeros(4)

    for i in range(4):
        delta[i] = i + 1

    normalize_online(timestamp, delta, mean, var)

    np.testing.assert_allclose(
        delta, [1, 1, 1, 1], rtol=1e-10, atol=0)

    np.testing.assert_allclose(
        mean, [0.5, 1, 1.5, 2], rtol=1e-10, atol=0)

    np.testing.assert_allclose(
        var, [0.5, 2, 4.5, 8], rtol=1e-10, atol=0)


def test_normalize_online_function_2():
    timestamp = 0
    delta = np.array([0.94412302, 0.86146408, 0.73341806, 0.61216245, 0.96908061, 0.97472264,
                      0.8408178, 0.96008555, 0.40090214], dtype=np.float64)
    mean = np.array([0.32338348, 0.99894723, 0.6193192, 0.97286237, 0.37726698, 0.05815544,
                     0.16665981, 0.02960246, 0.53373795], dtype=np.float64)
    var = np.array([0.64274297, 0.90765843, 0.4144643,  0.18930178, 0.02663542, 0.96685482,
                    0.37729824, 0.33513192, 0.1533], dtype=np.float64)

    normalize_online(timestamp, delta, mean, var)

    np.testing.assert_allclose(
        delta, [0.944123, 0.861464, 0.733418, 0.612162, 0.969081, 0.974723, 0.840818, 0.960086, 0.400902], rtol=1e-5)

    np.testing.assert_allclose(
        mean, [0.944123, 0.861464, 0.733418, 0.612162, 0.969081, 0.974723, 0.840818, 0.960086, 0.400902], rtol=1e-5, atol=0)

    np.testing.assert_allclose(
        var, [0.891368, 0.74212, 0.537902, 0.374743, 0.939117, 0.950084, 0.706975, 0.921764, 0.160723], rtol=1e-5, atol=0)


def test_normalize_online_function_3():
    timestamp = 1

    delta = np.array([0.88602986, 0.2131129, 0.94403679, 0.73892325,
                      0.44467259, 0.52709306, 0.90092566, 0.48505121], dtype=np.float64)
    mean = np.array([0.433028, 0.303627, 0.994544, 0.637347,
                     0.54407, 0.975582, 0.314164, 0.872511], dtype=np.float64)
    var = np.array([0.187513, 0.0921894, 0.989117, 0.406211,
                    0.296012, 0.951761, 0.0986991, 0.761275], dtype=np.float64)

    normalize_online(timestamp, delta, mean, var)

    np.testing.assert_allclose(
        delta, [1, -0.999995, -1.0003, 1.00002, -1.00002, -0.999996, 1, -1], rtol=1e-5)

    np.testing.assert_allclose(
        mean, [0.659529, 0.25837, 0.96929, 0.688135, 0.494371, 0.751338, 0.607545, 0.678781], rtol=1e-5, atol=0)

    np.testing.assert_allclose(
        var, [0.486281, 0.0688033, 0.940161, 0.476109, 0.246873, 0.614794, 0.455183, 0.498275], rtol=1e-5, atol=0)
