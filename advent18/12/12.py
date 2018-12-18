#!/usr/bin/env python3

import re
import collections
import sys
import os

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    data = [x.strip() for x in f.readlines()]

initial_state = data[0][15:]
searches_text = data[2:]

searches = set()
for line in searches_text:
    tokens = line.split(" => ")
    if tokens[1] != "#":
        continue
    s = tuple( True if x == '#' else False for x in tokens[0] )
    searches.add(s)



def get_estimate(gen_max):

    estimates = collections.Counter()

    state = set()
    for i, x in enumerate(initial_state):
        if x == "#":
            state.add(i)

    for g_index in range(gen_max):

        new_state = set()
        seen = set()

        for n in  state:
            for nn in range(-3, 6):

                nnn = n+nn
                if nnn not in seen:
                    view = tuple( x+nnn-2 in state for x in range(5) )
                    if view in searches:
                        new_state.add(nnn)
                    seen.add(nnn)

        state = new_state

        g = g_index+1

        state_sum = sum(state)
        estimate = sum(  x-g+gen_max for x in state   )

        estimates[estimate] += 1

        if DEBUG:
            print (f"g{g}: {state_sum}   |   g{gen_max}: {estimate} ")

        # make sure the estimate appears multiple times before returning
        if estimates[estimate] > 8:
            break

    return estimate


print(get_estimate(20))
print(get_estimate(50000000000))
