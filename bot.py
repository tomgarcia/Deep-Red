"""
Programmer-friendly interface to the neural network.
"""
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
            self.action_net = NeuralNet(input_size, 2, num_actions)
            self.action_samples = ([], [])

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
