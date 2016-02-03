"""Miscellaneous functions for dealing with cards."""
from random import randrange


def format_input(card, prev_card):
    """
    Format two cards in a manner that the decision tree can understand them.
    """
    if prev_card[0] < card[0]:
        rank = 0
    elif prev_card[0] == card[0]:
        rank = 1
    else:
        rank = 2
    suite = prev_card[1] == card[1]
    return card + prev_card + (rank, suite)


def deal(num_cards):
    """
    Deal a hand with the given number of cards. Cards are randomly generated,
    and therefore not guaranteed to be unique.
    """
    return [(randrange(13), randrange(4)) for i in range(num_cards)]


def tuple_from_s(s):
    """
    Create a tuple representing a card, based on its string
    representation.
    """
    if s == "":
        return False
    rank = s[:len(s)-1]
    suit = s[len(s)-1]
    if suit.lower() == 'c':
        suit = 0
    elif suit.lower() == 'd':
        suit = 1
    elif suit.lower() == 'h':
        suit = 2
    elif suit.lower() == 's':
        suit = 3
    else:
        return False

    if rank.isdigit() and int(rank) > 1 and int(rank) < 11:
        rank = int(rank) - 2
    elif rank.lower() == 'j':
        rank = 9
    elif rank.lower() == 'q':
        rank = 10
    elif rank.lower() == 'k':
        rank = 11
    elif rank.lower() == 'a':
        rank = 12
    else:
        return False
    return (rank, suit)


def s_from_tuple(t):
    """Convert a card tuple into its corresponding name."""
    rank, suit = t
    if rank == 12:
        s = "Ace"
    elif rank == 11:
        s = "King"
    elif rank == 10:
        s = "Queen"
    elif rank == 9:
        s = "Jack"
    else:
        s = str(rank + 2)

    if suit == 0:
        s += " of Clubs"
    elif suit == 1:
        s += " of Diamonds"
    elif suit == 2:
        s += " of Hearts"
    elif suit == 3:
        s += " of Spades"
    return s
