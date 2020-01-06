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

from copy import deepcopy

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = [ (x[0], int(x[1])) for x in re.findall("([LR])(\d+)", f.read()) ]
        return data

'''
 N
W E
 S
'''

def update_direction(direction, turn):
    return {
        ("N", "L"): "W",
        ("N", "R"): "E",

        ("S", "L"): "E",
        ("S", "R"): "W",

        ("E", "L"): "N",
        ("E", "R"): "S",

        ("W", "L"): "S",
        ("W", "R"): "N",
    }[ (direction, turn)]

def update_position(pos, direction, distance):
    if direction == "N":
        return (pos[0], pos[1]-distance)
    elif direction == "S":
        return (pos[0], pos[1]+distance)
    elif direction == "E":
        return (pos[0]+distance, pos[1])
    elif direction == "W":
        return (pos[0]-distance, pos[1])
    else:
        raise Exception(f'bad direction: {direction}')

def manhattan_distance(pa, pb):
    return abs(pa[0] - pb[0]) + abs(pa[1] - pb[1])


def part_1(data):

    pos = (0,0)
    direction = "N"

    for turn, distance in data:
        direction = update_direction(direction, turn)
        pos = update_position(pos, direction, distance)

    return (manhattan_distance( (0,0), pos))


def part_2(data):

    def generator(data):
        pos = (0,0)
        direction = "N"

        yield pos
        for turn, distance in data:
            direction = update_direction(direction, turn)
            for r in range(distance):
                pos = update_position(pos, direction, 1)
                yield pos

    seen = set()

    for pos in generator(data):
        if pos in seen:
            break
        seen.add(pos)
            
    return (manhattan_distance( (0,0), pos))


def main():
    data = load()

    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
