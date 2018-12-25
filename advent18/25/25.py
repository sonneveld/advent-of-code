#!/usr/bin/env python3

import re
import collections
import sys
import os
from heapq import heappush, heappop
from functools import lru_cache
import random

sys.setrecursionlimit(2000)

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

data = []
with open(input_filename) as f:
    for line in f:
        x,y,z,t = [int(x) for x in line.strip().split(',')]
        data.append(  (x,y,z,t) )

constellations = [set( [ (x,y,z,t) ] ) for x,y,z,t in data  ]

def calc_manhattan_distance(c1,c2):
    assert(len(c1) == 4)
    assert(len(c2) == 4)
    return sum( abs(y-x) for x,y in zip(c1, c2))

assert(  calc_manhattan_distance ((0,0,0,0), (3,0,0,0)) == 3   )
assert(  calc_manhattan_distance ((0,0,0,0), (0,3,0,0)) == 3   )
assert(  calc_manhattan_distance ((0,0,0,0), (0,0,3,0)) == 3   )
assert(  calc_manhattan_distance ((0,0,0,0), (0,0,0,3)) == 3   )

def is_same_constellation(c1,c2):
    for x in c1:
        for y in c2:
            if calc_manhattan_distance(x,y) <= 3:
                return True
    return False

things_changed = True
while things_changed:

    things_changed = False

    remaining = list(constellations)

    next_constellations = []

    while len(remaining) > 0:
        const = set(remaining.pop(0))
        for other in list(remaining):

            if is_same_constellation(const, other):
                const = const | other
                things_changed = True
                remaining.remove(other)

        next_constellations.append(const)

    constellations = next_constellations

# Part 1

print(len(constellations))
