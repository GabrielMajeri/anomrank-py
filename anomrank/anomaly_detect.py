import numpy as np


def normalize_online(delta, mean, var, timestamp):
    """Normalizes the input data using a rolling mean.
    It modifies in place the input arrays.

    Parameters
    ----------
    delta : numpy array, 4 rows, double
        The second order derivative which measure how pagerank is modifying
    mean : double
        The mean vector
    var : double
        The variance vector
    timestamp : double
        A moment of time
    """

    alpha = timestamp / (timestamp + 1)
    beta = 1 / (timestamp + 1)

    mean = alpha * mean + beta * delta
    var = alpha * var + beta * (delta * delta)

    std_dev = np.sqrt(var - (mean*mean))

    mask = (std_dev != 0)

    delta[mask] -= mean[mask]
    delta[mask] /= std_dev[mask]


def compute_first_derivative(t1, t2):
    return t2-t1


def compute_second_derivative(t1, t2, t3):
    return t3 - 2*t2 + t1


def compute_anomaly_score(timestamp, pagerank1,
                          pagerank2, mean, var):
    """ This function looks at the pagerank and if it changes quickly it means there is an anomaly in the network

    Parameters
    ----------
    timestamp : int
        A moment of time
    pagerank1 : numpy array, double
    pagerank2 : numpy array, double
    mean : numpy array, double
    var : numpy arrya, double
    """

    delta = np.zeros((4, mean.shape[0]))

    # Calculate the second order derivative to analyze how pagerank is modifying

    t_1 = (timestamp - 2) % 3
    t_2 = (timestamp - 1) % 3
    t_3 = timestamp % 3

    if timestamp > 0:
        delta[0] = compute_first_derivative(pagerank1[t_2], pagerank1[t_3])
        delta[2] = compute_first_derivative(pagerank2[t_2], pagerank2[t_3])

    if timestamp > 1:
        delta[1] = compute_second_derivative(
            pagerank1[t_1], pagerank1[t_2], pagerank1[t_3])
        delta[3] = compute_second_derivative(
            pagerank2[t_1], pagerank2[t_2], pagerank2[t_3])

    maxim = [0] * 4
    total_max = 1.0

    normalize_online(delta, mean, var, timestamp)

    maxim = np.amax(np.absolute(delta), axis=-1)

    total_max *= maxim

    delta_abs = np.absolute(delta)
    score_absum = np.sum(delta_abs)

    if timestamp <= 1:
        return -2000

    sub_score = score_absum * (total_max / maxim)

    score = np.max(sub_score)

    if score < -2000:
        score = -2000

    return score
