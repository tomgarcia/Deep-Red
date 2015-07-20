"""Miscellaneous functions for dealing with cards."""
def format_as_input(card):
    """
    Transform a simple representation (rank, suit) of a card
    into a format that is more useful for a neuralnet.
    Rank should be an integer from 0-12, and suit should be
    an integer from 0-3.
    """
    rank = [0,] * 13
    suit = [0, 0, 0, 0]
    rank[card[0]] = 1
    suit[card[1]] = 1
    return list(card) + rank + suit
