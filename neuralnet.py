"""Homegrown Neural Network Framework"""
import numpy as np
from scipy.optimize import minimize, check_grad
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

    def __call__(self, data):
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

    def check_gradient(self, input, expected_output):
        array, shapes = NeuralNet.unroll(self.weights)
        fun = lambda x: NeuralNet.cost(NeuralNet.roll(x, shapes), 
                                       input,
                                       expected_output)[0]
        grad = lambda x: NeuralNet.unroll(
                NeuralNet.cost(
                    NeuralNet.roll(x, shapes), input, expected_output)[1])[0]
        x = NeuralNet.roll(grad(array), shapes)[0]
        return check_grad(fun, grad, array)

    @staticmethod
    def cost(weights, input, expected_output):
        """
        Find the cost of the given weights,
        based on input and the expected_output.
        """
        input = np.asarray(input)
        expected_output = np.asarray(expected_output)
        # Single row "matrixes" are one-dimensional, not two,
        # so len() does not work as expected
        if len(input.shape) == 1:
            num_samples = 1
        else:
            num_samples = len(input)
        inputs = []
        results = []
        for weight in weights:
            # Sigmoid is the default activation function for neural nets
            inputs.append(input)
            result = sigmoid(input.dot(weight))
            results.append(result)
            input = result
        # This cost function is convex, unlike squared error,
        # which makes gradient descent easier
        error = (-expected_output * np.log(result) -
                 (1 - expected_output) * np.log(1 - result))
        cost = error.sum() / num_samples
        delta = result - expected_output
        deltas = [delta]
        for i in reversed(range(0, len(weights) - 1)):
            # g(x) (1- g(x)) is the derivative of sigmoid
            delta = (delta.dot(weights[i+1].transpose()) *
                     results[i] * (1 - results[i]))
            deltas.insert(0, delta)
        for delta in deltas:
            print(delta.shape)
        gradients = []
        for i in range(0, len(deltas)):
            gradients.append(inputs[i].transpose().dot(deltas[i]) / num_samples)
        for grad in gradients:
            print(grad.shape)
        print("")
        return cost, gradients

    @staticmethod
    def unroll(weights):
        w = weights[0].ravel()
        shapes = [weights[0].shape]
        for weight in weights[1:]:
            shapes.append(weight.shape)
            w = np.concatenate((w, weight.ravel()))
        return w, shapes

    @staticmethod
    def roll(array, shapes):
        splits = [0]
        for shape in shapes:
            splits.append(shape[0] * shape[1] + splits[len(splits)-1])
        splits = splits[1:len(splits)-1]
        weights = np.split(array, splits)
        for i in range(len(weights)):
            weights[i].shape = shapes[i]
        return weights
