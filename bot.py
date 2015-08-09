"""
Programmer-friendly interface to the neural network.
"""
import json

import numpy as np

from neuralnet import NeuralNet
from card import format_input


class Bot(object):
    """
    Object that wraps around the neural net, handling concepts
    such as "hand" and the list of previous plays.
    """

    def __init__(self, hand, actions=[]):
        """
        Creates a bot with an initial hand, and a list of actions
        that it can perform.
        """
        self.hand = hand
        input_size = len(format_input((0, 0), (0, 0)))
        self.valid_net = NeuralNet(input_size, 2, 1)
        self.valid_samples = ([], [])
        self.actions = actions
        self.action_samples = ([], [])
        self.action_net = NeuralNet(input_size, 2, len(self.actions))

    def add_sample(self, card, prev_card, is_valid, actions=[]):
        """
        Adds a new sample for the bot to train on. actions is
        not needed if the move is invalid, and must always be a list,
        even if there is only one action.
        """
        input = format_input(card, prev_card)
        self.valid_samples[0].append(input)
        self.valid_samples[1].append([int(is_valid)])
        self.valid_net.train(*self.valid_samples)
        if is_valid:
            self.action_samples[0].append(input)
            self.action_samples[1].append(actions)
            if self.actions:
                self.action_net.train(*self.action_samples)

    def add_card(self, card):
        """
        Adds a card to the bot's hand. The card should be a pair of ints.
        """
        self.hand.append(card)

    def play(self, prev_card):
        """
        Bot plays the best card from its hand, or passes by returning
        False. If bot plays a card, it also returns a list of actions.
        """
        if not self.hand:
            raise Exception("Empty Hand")
        input = [format_input(card, prev_card) for card in self.hand]
        output = self.valid_net(input)
        index = np.argmax(output, axis=0)
        if output[index] < .5:
            return False
        if self.actions:
            actions = np.rint(self.action_net([input[index]]))[0]
        else:
            actions = []
        return self.hand.pop(index), actions

    def add_action(self, action):
        self.actions.append(action)
        for output in self.action_samples[1]:
            output.append(0)
        output_weight = self.action_net.weights[len(self.action_net.weights)-1]
        rows, cols = output_weight.shape
        new_weight = np.resize(output_weight, (rows, cols+1))
        self.action_net.weights[len(self.action_net.weights)-1] = new_weight
        if self.action_samples[0]:
            self.action_net.train(*self.action_samples)

    def save(self, filename):
        """
        Save the bot's data to the given file, so it can be reloaded later.
        """
        f = open(filename, "w")
        obj = (self.hand,
               self.valid_samples,
               self.action_samples,
               self.actions)
        f.write(json.dumps(obj))

    @classmethod
    def load(cls, filename):
        """Create a new Bot from the file given."""
        f = open(filename, "r")
        bot = object.__new__(cls)
        bot.hand, \
            bot.valid_samples, \
            bot.action_samples, \
            bot.actions = json.loads(f.read())
        input_size = len(format_input((0, 0), (0, 0)))
        bot.valid_net = NeuralNet(input_size, 2, 1)
        num_actions = len(bot.actions)
        bot.action_net = NeuralNet(input_size, 2, num_actions)
        if bot.valid_samples[0]:
            bot.valid_net.train(*bot.valid_samples)
        if bot.action_samples[0]:
            bot.action_net.train(*bot.action_samples)
        return bot
