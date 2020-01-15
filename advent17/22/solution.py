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

from collections import Counter, defaultdict, namedtuple, deque
from copy import copy, deepcopy
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product, count, cycle, islice
from multiprocessing import Pool
from math import sqrt


DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = [x.rstrip() for x in f.readlines()]
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def update_pos(pos, direction):
    return pos[0]+direction[0], pos[1]+direction[1]

@lru_cache(None)
def turn_left(direction):
    if direction == (0, -1):  # up
        return (-1, 0)   #left
    elif direction == (0, 1):  # down
        return (1, 0)   # right
    if direction == (-1, 0):   # left
        return (0, 1)    # down
    elif direction == (1, 0):    #right
        return (0, -1)    # up
    else:
        raise Exception(f"bad direction: {direction}")

@lru_cache(None)
def turn_right(direction):
    if direction == (0, -1):  # up
        return (1, 0)   #left
    elif direction == (0, 1):  # down
        return (-1, 0)   # right
    if direction == (-1, 0):   # left
        return (0, -1)    # down
    elif direction == (1, 0):    #right
        return (0, 1)    # up
    else:
        raise Exception(f"bad direction: {direction}")

@lru_cache(None)
def turn_reverse(direction):
    return turn_right(turn_right(direction))


def part_1(data):

    state = defaultdict(bool)
    for y, row in enumerate(data):
        for x, ch in enumerate(row):
            if ch != "#":
                continue
            state[(x,y)] = True

    start_x = len(data[0]) // 2
    start_y = len(data) // 2

    pos = (start_x, start_y)
    direction = (0, -1)

    infection_bursts = 0

    for _ in range(10_000):

        if state[pos]:  # infected
            direction = turn_right(direction)
            state[pos] = False
        else:
            direction = turn_left(direction)
            state[pos] = True
            infection_bursts += 1

        pos = update_pos(pos, direction)


    return infection_bursts


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3

def part_2(data):

    state = defaultdict(int)
    for y, row in enumerate(data):
        for x, ch in enumerate(row):
            if ch != "#":
                continue
            state[(x,y)] = INFECTED

    start_x = len(data[0]) // 2
    start_y = len(data) // 2

    pos = (start_x, start_y)
    direction = (0, -1)

    infection_bursts = 0

    for _ in range(10_000_000):

        if state[pos] == CLEAN:
            direction = turn_left(direction)
            state[pos] = WEAKENED
        elif state[pos] == WEAKENED:
            # same direction
            state[pos] = INFECTED
            infection_bursts += 1
        elif state[pos] == INFECTED:
            direction = turn_right(direction)
            state[pos] = FLAGGED
        elif state[pos] == FLAGGED:
            direction = turn_reverse(direction)
            state[pos] = CLEAN
        else:
            raise Exception()

        pos = update_pos(pos, direction)

    return infection_bursts


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
