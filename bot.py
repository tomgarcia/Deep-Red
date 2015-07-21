"""
Programmer-friendly interface to the neural network.
"""
from neuralnet import NeuralNet
from card import format_as_input


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
        card_len = len(format_as_input((0, 0)))
        input_size = 2 * card_len + 2
        self.net = NeuralNet(input_size, 2, 1)
        self.samples = ([], [])

    def add_sample(self, card, prev_card, outcome):
        """Adds a new sample for the bot to train on."""
        card = format_as_input(card)
        prev_card = format_as_input(prev_card)
        matching = [int(card[0] == prev_card[0]),
                    int(card[1] == prev_card[1])]
        input = card + prev_card + matching
        self.samples[0].append(input)
        self.samples[1].append(outcome)
        self.net.train(self.samples[0], self.samples[1])

    def add_card(self, card):
        """
        Adds a card to the bot's hand. Currently not used
        for anything.
        """
        self.hand.append(card)
