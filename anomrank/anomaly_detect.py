import numpy as np


def normalize_online(timestamp, delta, mean, var):
    """Normalizes the input data using a rolling mean.
    It modifies in place the input arrays.

    Parameters
    ----------
    timestamp : double
        A moment of time
    delta : numpy array, 4 rows, double
        The second order derivative which measure how pagerank is modifying
    mean : double
        The mean vector
    var : double
        The variance vector
    """

    alpha = timestamp / (timestamp + 1)
    beta = 1 / (timestamp + 1)

    mean[:] = alpha * mean[:] + beta * delta[:]
    var[:] = alpha * var[:] + beta * (delta[:] * delta[:])

    print("Mean: ")
    print(mean)
    print("Var: ")
    print(var)

    std_dev = np.sqrt(var - (mean*mean))

    print(std_dev)

    mask = (std_dev != 0)

    delta[mask] -= mean[mask]
    delta[mask] /= std_dev[mask]


def compute_first_derivative(t1, t2):
    """Compute the first derivative using last two timestamps."""
    return t2-t1


def compute_second_derivative(t1, t2, t3):
    """Compute the second derivative using last three timestamps."""
    return t3 - 2*t2 + t1


def compute_anomaly_score(timestamp, pagerank1,
                          pagerank2, mean, var):
    """This function looks at the pagerank and if it changes quickly it means there is an anomaly in the network

    Parameters
    ----------
    timestamp : int
        A moment of time
    pagerank1 : numpy array, double
        Pagerank of network nodes using first algorithm
    pagerank2 : numpy array, double
        Pagerank of network nodes using second algorithm
    mean : numpy array, double
    var : numpy array, double
    """

    delta = np.zeros((4, len(mean[0])))

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

    normalize_online(timestamp, delta, mean, var)

    if timestamp <= 1:
        return -2000

    maxim = np.zeros(4)
    total_max = 1.0

    maxim = np.amax(np.absolute(delta), axis=-1)

    total_max = np.prod(maxim)

    delta_abs = np.absolute(delta)
    score_absum = np.sum(delta_abs)

    sub_score = score_absum * (total_max / maxim)

    score = np.max(sub_score)

    if score < -2000:
        score = -2000

    return score


def testing_localy():
    pagerank1 = np.array([[0.76133757, 0.95800655, 0.10948495, 0.16610539], [0.04689945, 0.66376899, 0.3712425, 0.71729884],
                          [0.23790798, 0.87033685, 0.72526328, 0.06117944], [0.86800126, 0.80570202, 0.26965533, 0.03903525]], dtype=np.float64)

    pagerank2 = np.array([[0.18710652, 0.61945598, 0.20482165, 0.71507528], [0.56840143, 0.15190741, 0.44738063, 0.63140366],
                          [0.99126372, 0.39077755, 0.76775062, 0.22622011], [0.68278319, 0.21806658, 0.48163308, 0.77215408]], dtype=np.float64)

    mean = np.array([[0.22724092, 0.04157759, 0.19641686, 0.8437104], [0.50581343, 0.19875327, 0.09752145, 0.08925034],
                     [0.50488943, 0.58094689, 0.00368728, 0.0063093], [0.53095188, 0.02988576, 0.52299029, 0.48807976]], dtype=np.float64)

    var = np.array([[0.50175159, 0.95379638, 0.94255591, 0.01186513], [0.77449294, 0.3350722, 0.75235295, 0.88804683],
                    [0.39686282, 0.88822454, 0.77616695, 0.44548273], [0.15980234, 0.79107864, 0.76585466, 0.55312671]], dtype=np.float64)
    compute_anomaly_score(1, pagerank1, pagerank2, mean, var)


# testing_localy()
