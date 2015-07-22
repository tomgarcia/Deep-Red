#!/usr/bin/python3
"""
Temporary script for testing ai.
"""
from bot import Bot
from card import deal

print("Starting Training")
ai = Bot(deal(5), 1)
for i in range(52):
    card, prev_card = deal(2)
    same_rank = card[0] == prev_card[0]
    same_suit = card[1] == prev_card[1]
    output = same_rank or same_suit
    if prev_card[0] == 5 and not card[0] >= 5:
        output = False
    elif prev_card[0] == 7 and not card[0] == 7:
        output = False
    if card[0] == prev_card[0]:
        tap = 1
    else:
        tap = 0
    ai.add_sample(card, prev_card, output, [tap])
print("Training Complete")
while True:
    prev_card = [int(s) for s in input("Enter top of pile: ").split()]
    print(ai.hand)
    play = ai.play(prev_card)
    if play:
        print(play)
        card, actions = play
        if input("valid?") == "n":
            ai.add_sample(card, prev_card, False)
        else:
            if input("correct actions?") == "n":
                actions = [int(s) for s in input("Correct actions: ").split()]
            ai.add_sample(card, prev_card, True, actions)
    else:
        print("Pass")
        ai.add_card(*deal(1))
