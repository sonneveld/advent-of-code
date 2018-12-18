#!/usr/bin/env python3

# NOTE: this works, but is very slow. Try 09.ipynb instead.

import re
import sys

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    data = f.read().strip()

init_num_players, init_max_marble = [int(x) for x in re.findall(r'\d+', data)][:2]


def calc_max_score(num_players, max_marble):
    state = [0]
    current = 0

    player_id = 0

    scores = [0]*num_players

    for m in range(1, max_marble+1):

        if m % 23 == 0:
            scores[player_id] += m
            new_current = (current - 7)%len(state)
            scores[player_id] += state.pop(new_current)
            current = new_current
        else:
            new_current = (current + 2)%len(state)
            if new_current == 0:
                new_current = len(state)
            state.insert(new_current, m)
            current = new_current

        player_id = (player_id + 1)%num_players

    return max(scores)


print (calc_max_score(init_num_players, init_max_marble))
print (calc_max_score(init_num_players, init_max_marble*100))
