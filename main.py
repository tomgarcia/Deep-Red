#!/usr/bin/python3
"""
Temporary script for testing ai.
"""
from bot import Bot
from card import deal

print("Starting Training")
ai = Bot(deal(5))
for i in range(100):
    card1, card2 = deal(2)
    same_rank = card1[0] == card2[0]
    same_suit = card1[1] == card2[1]
    output = int(same_rank or same_suit)
    ai.add_sample(card1, card2, (output,))
print("Training Complete")
net = ai.net
while True:
    data = [int(s) for s in input("Enter top of pile: ").split()]
    prev_card = (data[0], data[1])
    print(ai.hand)
    card = ai.play(prev_card)
    print(card)
    ai.add_card(*deal(1))
    correct_output = int(input("Valid?(1/0): "))
    ai.add_sample(card, prev_card, (correct_output,))
