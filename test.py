#!/usr/bin/env python3
from neuralnet import NeuralNet
from card import deal, format_input


def get_test_data(num_training, num_validation, num_test):
    samples = {"training": ([], []), "validation": ([], []), "test": ([], [])}
    num_samples = {"training": num_training, "validation": num_validation, "test": num_test}
    for key, count in num_samples.items():
        for i in range(count):
            for j in range(2):
                samples[key][j].append(make_sample(*deal(2))[j])
    return samples


def make_sample(card, prev_card):
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


input_size = len(format_input((0, 0), (0, 0)))
samples = get_test_data(52, 17, 17)
nets = [NeuralNet(input_size, 2, 1), NeuralNet(input_size, 2, 2, 1), NeuralNet(input_size, 1)]
for net in nets:
    net.train(*samples["training"])
    print("---")
    print("Training Cost:", NeuralNet.cost(net.weights, net.lambda_, *samples["training"])[0])
    print("Validation Cost:", NeuralNet.cost(net.weights, net.lambda_, *samples["validation"])[0])
    print("Test Cost:", NeuralNet.cost(net.weights, net.lambda_, *samples["test"])[0])
