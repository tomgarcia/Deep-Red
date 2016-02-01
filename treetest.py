#!/usr/bin/python
import numpy as np
from decisiontree import DecisionTree
from card import deal, format_input

def get_test_data(num_training, num_validation, fun):
    samples = {"training": [], "validation": []}
    num_samples = {"training": num_training,
                   "validation": num_validation}
    for key, count in num_samples.items():
        for i in range(count):
            samples[key].append(fun(*deal(2)))
    for key in samples.keys():
        samples[key] = np.array(samples[key])
    return samples


def make_play_sample(card, prev_card):
    if prev_card[0] < card[0]:
        rank = 0
    elif prev_card[0] == card[0]:
        rank = 1
    else:
        rank = 2
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

def make_action_sample(card, prev_card):
    if prev_card[0] < card[0]:
        rank = 0
    elif prev_card[0] == card[0]:
        rank = 1
    else:
        rank = 2
    suite = prev_card[1] == card[1]
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
    return [actions, *card, *prev_card, rank, suite]

def percent_correct(samples, schema):
    d = DecisionTree(samples["training"], schema)
    for key in samples.keys():
        print(key)
        correct = 0
        for sample in samples[key]:
            if d(sample[1:]) == sample[0]:
                correct += 1
        print((correct / len(samples[key])) * 100)

print("Play Test")
samples = get_test_data(20, 100000, make_play_sample)
percent_correct(samples, [2, 13, 4, 13, 4, 3, 2])

print("Action Test")
for i in range(5):
    print("Action #" + str(i+1))

    def f(card, prev_card):
        sample = make_action_sample(card, prev_card)
        cls = sample[0][1]
        return [cls, *sample[1:]]

    samples = get_test_data(20, 100000, f)
    percent_correct(samples, [4, 13, 4, 13, 4, 3, 2])
