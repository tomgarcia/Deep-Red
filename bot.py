"""
Programmer-friendly interface to the neural network.
"""
#TODO: play()
import json

import numpy as np

from decisiontree import DecisionTree
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
        self.valid_samples = []
        self.actions = actions
        # Create one list per action
        self.action_samples = [[]] * len(self.actions)

    def add_sample(self, card, prev_card, is_valid, actions=[]):
        """
        Adds a new sample for the bot to train on. actions is
        not needed if the move is invalid, and must always be a list,
        even if there is only one action.
        """
        sample = format_input(card, prev_card)
        self.valid_samples.append([is_valid, *sample])
        if is_valid:
            for i in range(len(actions)):
                self.action_samples[i].append([actions[i], *sample])

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
            for i in range(len(actions)):
                if actions[i] < 0:
                    actions[i] = 0
        else:
            actions = []
        return self.hand.pop(index), actions

    def add_action(self, action):
        self.actions.append(action)
        for sample in self.valid_samples:
            if sample[0] == True:
                self.action_samples[len(self.actions)-1].append([0, *sample])

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
        return bot
