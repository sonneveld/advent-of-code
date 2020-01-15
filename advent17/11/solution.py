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
        data = re.findall('\w+', f.read())
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

# reference https://www.redblobgames.com/grids/hexagons/
#  N
# W E
#  S

DIRECTIONS = ('n', 's', 'nw',  'sw', 'ne', 'se', )

@lru_cache(None)
def update_hex_pos(pos, direction):
    
    if direction == "n":
        return pos[0], pos[1]-1
    elif direction == "s":
        return pos[0], pos[1]+1

    if pos[0] % 2 == 0: # even
        if direction == "nw":
            return pos[0]-1, pos[1]-1
        elif direction == "sw":
            return pos[0]-1, pos[1]
        elif direction == "ne":
            return pos[0]+1, pos[1] -1
        elif direction == "se":
            return pos[0]+1, pos[1]
    else: #odd
        if direction == "nw":
            return pos[0]-1, pos[1]
        elif direction == "sw":
            return pos[0]-1, pos[1]+1
        elif direction == "ne":
            return pos[0]+1, pos[1]
        elif direction == "se":
            return pos[0]+1, pos[1]+1

    raise Exception(f"bad direction {pos} {direction}")


@lru_cache(None)
def shortest_hex_path_slow(src, dest):

    q = deque()
    q.appendleft( (0, src) )

    seen = set()

    while q:

        steps, p = q.pop()
        if p in seen:
            continue

        if p == dest:
            return steps
        seen.add(p)

        next_steps = steps + 1
        for d in DIRECTIONS:
            next_p = update_hex_pos(p, d)
            if next_p in seen:
                continue
            q.appendleft( (next_steps, next_p))


def manhattan_distance(pa, pb):
    return abs(pa[0] - pb[0]) + abs(pa[1] - pb[1])

@lru_cache(None)
def shortest_hex_path(src, dest):

    q = []

    def push(steps, pos):
        distance_left = manhattan_distance(pos, dest)
        steps_left = -steps
        heapq.heappush(q, (distance_left, steps_left, steps, pos))

    def pop():
        _, _, steps, p = heapq.heappop(q)
        return steps, p

    init_pos = src
    push(0, init_pos)

    seen = set()

    while q:

        steps, p = pop()
        if p in seen:
            continue

        if p == dest:
            return steps
        seen.add(p)

        next_steps = steps + 1
        for d in DIRECTIONS:
            next_p = update_hex_pos(p, d)
            if next_p in seen:
                continue
            push(next_steps, next_p)


def part_1(data):

    p = (0,0)

    for d in data:
        p = update_hex_pos(p, d)

    return shortest_hex_path( (0,0), p)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):

    p = (0,0)

    seen = set()
    seen.add(p)

    for d in data:
        p = update_hex_pos(p, d)
        seen.add(p)

    # sort furthest points first
    seen = list(seen)
    seen.sort(key= lambda p: abs(p[0]) + abs(p[1]), reverse=True)

    distances = set()
    for i, p in enumerate(seen):
        distances.add(  shortest_hex_path( (0,0), p) )
        # early exit since it's probably found
        if i > 50: break

    return max(distances)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
