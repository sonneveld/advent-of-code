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
from itertools import combinations, permutations, product, count, cycle, islice, chain
from multiprocessing import Pool
from math import sqrt

from knothash import hashit_b

DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        return f.read().strip()


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def hashit_bits(s):

    buf = hashit_b(s)
    for b in buf:
        for x in range(8):
            yield (b & 0x80) >> 7
            b <<= 1

def gen_used_map(data):
    used = {}
    for y in range(128):
        s = f'{data}-{y}'
        for x, v in islice(enumerate(hashit_bits(s)), 0, 128):
            used[(x,y)] = v
    return used

def part_1(data):
    used = gen_used_map(data)
    return list(used.values()).count(True)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )

def group_from_pos(points, init_pos):
    q = set()
    q.add(init_pos)
    seen = set()

    while q:
        p = q.pop()

        if p in seen:
            continue
        seen.add(p)

        for a in get_adj_pos(p):
            if a in seen:
                continue
            if a not in points:
                continue
            q.add(a)
    return seen

def part_2(data):
    used = gen_used_map(data)

    all_points = set(p for p,v in used.items() if v)
    ungrouped_points = set(all_points)

    group_count = 0
    while ungrouped_points:
        p = ungrouped_points.pop()
        group = group_from_pos(all_points, p)
        ungrouped_points -= group
        group_count += 1

    return group_count


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
