#!/usr/bin/env python3
import numpy as np

from neuralnet import NeuralNet
from card import deal, format_input


def get_test_data(num_training, num_validation, num_test, fun):
    samples = {"training": ([], []), "validation": ([], []), "test": ([], [])}
    num_samples = {"training": num_training,
                   "validation": num_validation,
                   "test": num_test}
    for key, count in num_samples.items():
        for i in range(count):
            for j in range(2):
                samples[key][j].append(fun(*deal(2))[j])
    return samples


def make_play_sample(card, prev_card):
    if prev_card[0] == card[0]:
        is_correct = 1
    elif prev_card[1] == card[1]:
        if prev_card[0] == 3 and card[0] < 3:
            is_correct = 0
        elif prev_card[0] == 5 and card[0] != 5:
            is_correct = 0
        else:
            is_correct = 1
    else:
        is_correct = 0
    return [format_input(card, prev_card), [is_correct]]


def make_action_sample(card, prev_card):
    actions = [0, 0, 0, 0, 0]
    if prev_card[0] == card[0]:
        actions[0] = 1
    if card[0] == 5 or card[0] == 3 or card[1] == 2 or card[1] == 3:
        actions[1] = 1
    if card[0] > 8:
        actions[2] = card[0] - 8
    if card[0] == 8:
        actions[3] = 1
    if card[0] == 0:
        actions[4] = 1
    return [format_input(card, prev_card), actions]


def percent_error(net, input, expected_output):
    num_wrong = 0
    total = 0
    output = net(input)
    output = np.rint(net(input))
    for i in range(len(output)):
        total += len(output[i])
        for j in range(len(output[i])):
            if output[i][j] != expected_output[i][j]:
                num_wrong += 1
    return (num_wrong / total) * 100


input_size = len(format_input((0, 0), (0, 0)))
print("Start of Play Test")
samples = get_test_data(520, 1000, 1000, make_play_sample)
nets = [
        NeuralNet(input_size, 2, 1, lambda_=0),
        NeuralNet(input_size, 4, 1, lambda_=0),
        NeuralNet(input_size, 8, 1, lambda_=0),
        NeuralNet(input_size, 8, 4, 1, lambda_=0),
        ]
for net in nets:
    net.train(*samples["training"])
    print("---")
    print("Training")
    print("Error %: {}, Cost: {}".format(
        round(percent_error(net, *samples["training"]), 2),
        NeuralNet.cost(net.weights, net.lambda_, *samples["training"])[0]))
    print("Validation")
    print("Error %: {}, Cost: {}".format(
        round(percent_error(net, *samples["validation"]), 2),
        NeuralNet.cost(net.weights, net.lambda_, *samples["validation"])[0]))
    print("Test")
    print("Error %: {}, Cost: {}".format(
        round(percent_error(net, *samples["test"]), 2),
        NeuralNet.cost(net.weights, net.lambda_, *samples["test"])[0]))
print("\n")
print("Start Of Action Test")
samples = get_test_data(52, 170, 170, make_action_sample)
nets = [
        #NeuralNet(input_size, 2, 5),
        #NeuralNet(input_size, 5, 5),
        #NeuralNet(input_size, 3, 5),
        #NeuralNet(input_size, 5, 5),
        ]
for net in nets:
    net.train(*samples["training"])
    print("---")
    print("Training")
    print("Error %: {}, Cost: {}".format(
        round(percent_error(net, *samples["training"]), 2),
        NeuralNet.cost(net.weights, net.lambda_, *samples["training"])[0]))
    print("Validation")
    print("Error %: {}, Cost: {}".format(
        round(percent_error(net, *samples["validation"]), 2),
        NeuralNet.cost(net.weights, net.lambda_, *samples["validation"])[0]))
    print("Test")
    print("Error %: {}, Cost: {}".format(
        round(percent_error(net, *samples["test"]), 2),
        NeuralNet.cost(net.weights, net.lambda_, *samples["test"])[0]))
