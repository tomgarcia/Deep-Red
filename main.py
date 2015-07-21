#!/usr/bin/python3
import numpy as np
from random import randrange

from bot import Bot
from card import format_as_input

print("Starting Training")
ai = Bot([])
for i in range(100):
    card1 = (randrange(13), randrange(4))
    card2 = (randrange(13), randrange(4))
    same_rank = card1[0] == card2[0]
    same_suit = card1[1] == card2[1]
    output = int(same_rank or same_suit)
    ai.add_sample(card1, card2, (output,))
print("Training Complete")
net = ai.net
while True:
    data = [int(s) for s in input("Enter input: ").split()]
    card = format_as_input((data[0], data[1]))
    prev_card = format_as_input((data[2], data[3]))
    matching = [int(card[0] == prev_card[0]),
                int(card[1] == prev_card[1])]
    data = np.array([card + prev_card + matching])
    print(net(data))
