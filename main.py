#!/usr/bin/python3
import numpy as np
import sys
from random import randrange

from neuralnet import NeuralNet

print("Starting Training")
inputs = []
outputs = []
for i in range(50):
    card1 = (randrange(13), randrange(4))
    card2 = (randrange(13), randrange(4))
    same_rank = card1[0] == card2[0]
    same_suit = card1[1] == card2[1]
    output = same_rank or same_suit
    inputs.append([card1[0], card1[1], card2[0], card2[1], int(same_rank), int(same_suit)])
    outputs.append([int(output)])
net = NeuralNet(6, 1)
net.train(inputs, outputs)
print("Training Complete")
while True:
    data = [int(s) for s in input("Enter input: ").split()]
    data = np.array([data])
    print(net(data))
