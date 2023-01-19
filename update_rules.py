import numpy as np


def theta(t1, t2):
    return 1 if t1 == t2 else 0


def hebbian(weights, input_val, sigma, tau1, tau2, max_value):
    for (i, j), _ in np.ndenumerate(weights):
        weights[i, j] = weights[i, j] + input_val[i, j] * tau1 * theta(sigma[i], tau1) * theta(tau1, tau2)
        weights[i, j] = np.clip(weights[i, j], -max_value, max_value)
    return weights


def anti_hebbian(weights, input_val, sigma, tau1, tau2, max_value):

    for (i, j), _ in np.ndenumerate(weights):
        weights[i, j] -= input_val[i, j] * tau1 * theta(sigma[i], tau1) * theta(tau1, tau2)
        weights[i, j] = np.clip(weights[i, j], -max_value, max_value)
    return weights


def random_walk(weights, input_val, sigma, tau1, tau2, max_value):
    for (i, j), _ in np.ndenumerate(weights):
        weights[i, j] += input_val[i, j] * theta(sigma[i], tau1) * theta(tau1, tau2)
        weights[i, j] = np.clip(weights[i, j], -max_value, max_value)
    return weights
