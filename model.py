import numpy as np
from update_rules import hebbian, anti_hebbian, random_walk
from math import sqrt


class TPM:
    def __init__(self, input_size=4, hidden_size=3, max_value=6):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.max_value = max_value
        self.weights = np.random.randint(-max_value, max_value + 1, [hidden_size, input_size])
        self.sigma = 0
        self.tau = 0
        self.input_val = None

    def get_output(self, input_val):

        hidden_size = self.hidden_size
        input_size = self.input_size
        weights = self.weights

        input_val = input_val.reshape([hidden_size, input_size])

        sigma = np.sign(np.sum(input_val * weights, axis=1) * (1/sqrt(len(input_val))))
        for i, _ in np.ndenumerate(sigma):
            if sigma[i] == 0:
                sigma[i] = -1

        tau = np.prod(sigma)
        self.input_val = input_val
        self.sigma = sigma
        self.tau = tau

        return self.tau

    def __call__(self, input_val):
        return self.get_output(input_val)

    def update(self, second_tau, update_rule='hebbian'):

        if self.tau == second_tau:
            if update_rule == 'hebbian':
                self.weights = hebbian(self.weights, self.input_val,
                                       self.sigma, self.tau, second_tau, self.max_value)

            elif update_rule == 'anti_hebbian':
                self.weights = anti_hebbian(self.weights, self.input_val,
                                            self.sigma, self.tau, second_tau, self.max_value)

            elif update_rule == 'random_walk':
                self.weights = random_walk(self.weights, self.input_val,
                                           self.sigma, self.tau, second_tau, self.max_value)
            else:
                raise Exception("Invalid update rule.")
