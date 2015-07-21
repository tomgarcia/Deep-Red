"""Miscellaneous functions for dealing with cards."""
from random import randrange


def format_as_input(card):
    """
    Transform a simple representation (rank, suit) of a card
    into a format that is more useful for a neuralnet.
    Rank should be an integer from 0-12, and suit should be
    an integer from 0-3.
    """
    rank = [0, ] * 13
    suit = [0, 0, 0, 0]
    rank[card[0]] = 1
    suit[card[1]] = 1
    return list(card) + rank + suit


def deal(num_cards):
    """
    Deal a hand with the given number of cards. Cards are randomly generated,
    and therefore not guaranteed to be unique.
    """
    return [(randrange(13), randrange(4)) for i in range(num_cards)]
