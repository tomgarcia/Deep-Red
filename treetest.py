#!/usr/bin/python
import numpy as np
from decisiontree import DecisionTree
from card import deal

def get_test_data(num_training, num_validation, num_test, fun):
    samples = {"training": [], "validation": [], "test": []}
    num_samples = {"training": num_training,
                   "validation": num_validation,
                   "test": num_test}
    for key, count in num_samples.items():
        for i in range(count):
            samples[key].append(fun(*deal(2)))
    for key in samples.keys():
        samples[key] = np.array(samples[key])
    return samples


def make_play_sample(card, prev_card):
    rank = prev_card[0] == card[0]
    suite = prev_card[1] == card[1]
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
    return [is_correct, *card, *prev_card, rank, suite]

samples = get_test_data(100, 1000, 1000, make_play_sample)
d = DecisionTree(samples["training"], [2, 13, 4, 13, 4, 2, 2])
for key in samples.keys():
    print(key)
    correct = 0
    for sample in samples[key]:
        if d(sample[1:]) == sample[0]:
            correct += 1
    print((correct / len(samples[key])) * 100)
