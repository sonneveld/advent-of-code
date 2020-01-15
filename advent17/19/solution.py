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


def path_generator(track, start_pos):

    pos = start_pos
    direction = (0, 1)

    while True:

        assert pos in track

        yield pos

        next_pos = update_pos(pos, direction)
        next_direction = direction

        # try left
        if next_pos not in track:
            next_direction = turn_left(direction)
            next_pos = update_pos(pos, next_direction)

        # try right
        if next_pos not in track:
            next_direction = turn_right(direction)
            next_pos = update_pos(pos, next_direction)

        if next_pos not in track:
            break

        pos = next_pos
        direction = next_direction


def part_1(data):

    letters = {}
    track = {}
    for y, row in enumerate(data):
        for x, ch in enumerate(row):
            if ch == " ":
                continue
            track[(x,y)] = True
            if ch in string.ascii_letters:
                letters[(x,y)] = ch

    start_x = data[0].index("|")
    start_y = 0

    result = []
    for pos in path_generator(track, (start_x, start_y)):
        if pos in letters:
            result.append(letters[pos])

    return ''.join(result)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):

    letters = {}
    track = {}
    for y, row in enumerate(data):
        for x, ch in enumerate(row):
            if ch == " ":
                continue
            track[(x,y)] = True
            if ch in string.ascii_letters:
                letters[(x,y)] = ch

    start_x = data[0].index("|")
    start_y = 0

    result = []
    steps = 0
    for pos in path_generator(track, (start_x, start_y)):
        steps += 1
        if pos in letters:
            result.append(letters[pos])
        if len(result) == len(letters):
            break

    return steps


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
