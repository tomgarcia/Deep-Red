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

    def __init__(self, hand):
        """
        Creates a bot with an initial hand.
        hands are not currently used for anything.
        """
        self.hand = hand
        input_size = len(format_input((0, 0), (0, 0)))
        self.net = NeuralNet(input_size, 2, 1)
        self.samples = ([], [])

    def add_sample(self, card, prev_card, outcome):
        """Adds a new sample for the bot to train on."""
        input = format_input(card, prev_card)
        self.samples[0].append(input)
        self.samples[1].append(outcome)
        self.net.train(self.samples[0], self.samples[1])

    def add_card(self, card):
        """
        Adds a card to the bot's hand. Currently not used
        for anything.
        """
        self.hand.append(card)

    def play(self, prev_card):
        """
        Bot plays the best card from its hand, based on the card
        on top of the pile.
        """
        input = [format_input(card, prev_card) for card in self.hand]
        output = self.net(input)
        return self.hand.pop(np.argmax(output))
