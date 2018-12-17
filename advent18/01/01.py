#!/usr/bin/env python3

import itertools
import collections
import sys


try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

def load_changes():
    with open(input_filename) as f:
        for l in f:
            change = int(l.strip())
            yield change

changes = list(load_changes())


# Part 1

print (sum(changes))


# Part 2

freq_counter = [0]*1_000_000

freq = 0
freq_counter[freq] += 1

for change in itertools.cycle(changes):

    freq += change
    freq_counter[freq] += 1

    if freq_counter[freq] > 1:
        break

print (freq)
