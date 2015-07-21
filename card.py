"""Miscellaneous functions for dealing with cards."""
from random import randrange


def format_card(card):
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


def format_input(card, prev_card):
    card = format_card(card)
    prev_card = format_card(prev_card)
    matching = [int(card[0] == prev_card[0]),
                int(card[1] == prev_card[1])]
    return card + prev_card + matching


def deal(num_cards):
    """
    Deal a hand with the given number of cards. Cards are randomly generated,
    and therefore not guaranteed to be unique.
    """
    return [(randrange(13), randrange(4)) for i in range(num_cards)]
