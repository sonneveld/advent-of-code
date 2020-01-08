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

from copy import deepcopy

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = int(f.read())
        return data


@lru_cache(None)
def get_cell(x, y, modifier):
    v = x*x + 3*x + 2*x*y + y + y*y
    v += modifier
    num_bits = bin(v).count("1")
    return "." if num_bits%2 == 0 else "#"

def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )

def part_1(data):

    q = []
    init_pos = (1,1)
    seen = {}
    seen[init_pos] = 0
    q.append( (init_pos, 0) )

    while q:
        # print(len(q), q)
        pos,dist = q.pop(0)

        if pos not in seen or dist < seen[pos]:
            seen[pos] = dist

        if pos == (31,39):
            return dist

        next_dist = dist+1
        for next_pos in get_adj_pos(pos):
            c = get_cell(next_pos[0], next_pos[1], data)
            if c == "#":
                continue
            if next_pos[0] < 0:
                continue
            if next_pos[1] < 0:
                continue
            if next_pos in seen and next_dist >= seen[next_pos]:
                continue
            q.append( (next_pos, next_dist))


def part_2(data):

    q = []
    init_pos = (1,1)
    seen = {}
    seen[init_pos] = 0
    q.append( (init_pos, 0) )

    # The "maze" seems to not be infinite, this will eventually exit.

    while q:

        # print(len(q), q)
        pos,dist = q.pop(0)

        if pos not in seen or dist < seen[pos]:
            seen[pos] = dist

        next_dist = dist+1
        for next_pos in get_adj_pos(pos):
            c = get_cell(next_pos[0], next_pos[1], data)
            if c == "#":
                continue
            if next_pos[0] < 0:
                continue
            if next_pos[1] < 0:
                continue
            if next_pos in seen and next_dist >= seen[next_pos]:
                continue
            q.append( (next_pos, next_dist))

    return sum(1 for x in seen.values() if x <= 50)


def main():
    data = load()

    for y in range(40):
        for x in range(40):
            print(get_cell(x, y, data), end ='')
        print()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
