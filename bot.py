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

    def __init__(self, hand, num_actions):
        """
        Creates a bot with an initial hand, and a set number of
        actions to potentially perform.
        """
        self.hand = hand
        input_size = len(format_input((0, 0), (0, 0)))
        self.valid_net = NeuralNet(input_size, 2, 1)
        self.valid_samples = ([], [])
        self.has_actions = False
        if num_actions > 0:
            self.has_actions = True
            self.action_samples = ([], [])
            self.action_net = NeuralNet(input_size, 2, num_actions)

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
        if is_valid and self.has_actions:
            self.action_samples[0].append(input)
            self.action_samples[1].append(actions)
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
        if self.has_actions:
            actions = np.rint(self.action_net([input[index]]))[0]
        else:
            actions = []
        return self.hand.pop(index), actions

    def save(self, filename):
        """Save the bot's data to the given file, so it can be reloaded later."""
        f = open(filename, "w")
        if self.has_actions:
            f.write(json.dumps((self.hand, self.valid_samples, self.action_samples)))
        else:
            f.write(json.dumps((self.hand, self.valid_samples, False)))

    @classmethod
    def load(cls, filename):
        """Create a new Bot from the file given."""
        f = open(filename, "r")
        bot = object.__new__(cls)
        bot.hand, bot.valid_samples, action_samples = json.loads(f.read())
        input_size = len(format_input((0, 0), (0, 0)))
        bot.valid_net = NeuralNet(input_size, 2, 1)
        if bot.valid_samples[0]:
            bot.valid_net.train(*bot.valid_samples)
        if action_samples:
            bot.action_samples = action_samples
            num_actions = len(bot.action_samples[1][0])
            bot.has_actions = True
            bot.action_net = NeuralNet(input_size, 2, num_actions)
            bot.action_net.train(*bot.action_samples)
        else:
            bot.has_actions = False
        return bot
