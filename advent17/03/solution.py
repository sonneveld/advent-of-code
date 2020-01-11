#!/usr/bin/env python3

import sys
import os
import os.path
import re

import collections
import functools
import heapq
import itertools
import math
import multiprocessing
import random
import string
import time
import json
import hashlib

from collections import Counter
from collections import defaultdict
from collections import namedtuple
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import permutations
from itertools import product
from multiprocessing import Pool
from math import sqrt

from copy import copy, deepcopy

DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        return int(f.read())


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def adjust_anti_clockwise(direction):
    if direction == (0, -1):  # up
        return (-1, 0)
    elif direction == (0, 1):  # down
        return (1, 0)
    elif direction == (-1, 0):  # left
        return (0, 1)
    elif direction == (1, 0):   # right
        return (0, -1)
    else:
        raise Exception(f"bad direction:{direction}")

def adjust_pos(pos, direction):
    return pos[0]+direction[0], pos[1]+direction[1]

def spiral_gen():

    points_seen = set()

    pos = (0,0)
    v = 1
    direction = (0, 1) # down

    while True:
        points_seen.add(pos)
        yield pos, v

        v += 1

        turn_direction = adjust_anti_clockwise(direction)
        turn_pos = adjust_pos(pos, turn_direction)
        if turn_pos not in points_seen:
            pos = turn_pos
            direction = turn_direction
        else:
            pos = adjust_pos(pos, direction)

def dump_state(state):

    min_x = min(p[0] for p in state.keys())
    max_x = max(p[0] for p in state.keys())
    min_y = min(p[1] for p in state.keys())
    max_y = max(p[1] for p in state.keys())

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in state:
                print("%4d"% state[(x,y)], end =' ')
            else:
                print("    ", end = ' ')
        print()


def manhattan_distance(pa, pb):
    return abs(pa[0] - pb[0]) + abs(pa[1] - pb[1])

def part_1(data):

    state = {}

    for pos, v in spiral_gen():
        if DEBUG:
            state[pos] = v
            print()
            dump_state(state)

        if v == data:
            break

    return manhattan_distance( (0,0), pos)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def get_adj_pos(pos):

    return (
        (pos[0]-1, pos[1]-1),
        (pos[0]-1, pos[1]),
        (pos[0]-1, pos[1]+1),

        (pos[0], pos[1]-1),
        (pos[0], pos[1]+1),

        (pos[0]+1, pos[1]-1),
        (pos[0]+1, pos[1]),
        (pos[0]+1, pos[1]+1),
    )


def spiral_sums_gen():

    points_seen = {}

    pos = (0,0)
    v = 1
    direction = (0, 1) # down

    points_seen[pos] = 1

    while True:
        if pos == (0,0):
            v = 1
        else:
            # sum of adj
            v = 0
            for apos in get_adj_pos(pos):
                if apos in points_seen:
                    v += points_seen[apos]

        points_seen[pos] = v
        yield pos, v

        turn_direction = adjust_anti_clockwise(direction)
        turn_pos = adjust_pos(pos, turn_direction)
        if turn_pos not in points_seen:
            pos = turn_pos
            direction = turn_direction
        else:
            pos = adjust_pos(pos, direction)


def part_2(data):
    state = {}
    for pos, v in spiral_sums_gen():
        if DEBUG:
            state[pos] = v
            print()
            dump_state(state)

        if v > data:
            break

    return v


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
