"""Homegrown Neural Network Framework"""
import numpy as np
from scipy.special import expit as sigmoid


class NeuralNet(object):
    """A multi-layer, feed-forward neural network."""

    def __init__(self, *layers):
        """
        Parameters are a series of integers, each representing
        the number of nodes in one layer of the network. The first
        parameter is the number of inputs and the last is the number
        of outputs, so there is a minimum of two parameters.
        """
        if len(layers) < 2:
            raise Exception("Neural Net requires at least 2 layers")
        self.weights = []
        for i in range(len(layers) - 1):
            # TODO Find correct range for initial values
            self.weights.append(
                np.random.uniform(-1, 1, [layers[i], layers[i + 1]]))

    def compute(self, data):
        """
        Compute the network's function based on the input data.

        Data should be a two-dimensional array, where each row
        represents a sample, and each column represents a feature.
        The output is also an ndarray, where each row is a sample,
        and each column is an output feature.
        """
        for weight in self.weights:
            # Sigmoid is the default activation function for neural nets
            data = sigmoid(np.dot(data, weight))
        return data
