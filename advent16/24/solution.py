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

DEBUG=False


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            data.append(l.rstrip())
        return data


def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )

def shortest_path(open_spaces, src, dest):

    assert src in open_spaces
    assert dest in open_spaces

    init_steps = 0
    init_pos = src

    q = collections.deque()
    seen = set()

    q.appendleft ((init_steps, init_pos))

    while q:

        steps, pos = q.pop()

        if pos == dest:
            return steps

        if pos in seen:
            continue

        seen.add(pos)

        next_steps = steps + 1
        for next_pos in get_adj_pos(pos):
            if next_pos not in open_spaces:
                continue

            if next_pos in seen:
                continue

            q.appendleft( (next_steps, next_pos) )
            

def solution(data, return_to_base=False):

    pois = {}
    open_spaces = set()

    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            if ch != "#":
                open_spaces.add((x,y))
            if ch in "0123456789":
                point = int(ch)
                pois[point] = (x,y)

    poi_dist = {}

    for src, dest in product(pois.keys(), repeat=2):
        sp = shortest_path(open_spaces, pois[src], pois[dest])
        poi_dist[(src,dest)] = sp

    result = set()
    non_zero_pots = [x for x in pois.keys() if x != 0]
    for path in permutations(non_zero_pots):
        p = 0
        path = list(path)
        steps = 0
        while path:
            n = path.pop(0)
            dist = poi_dist[(p, n)]
            steps += dist
            p = n
        if return_to_base:
            steps += poi_dist[(p, 0)]
        result.add(steps)

    return min(result)


def part_1(data):
    return solution(data)

def part_2(data):
    return solution(data, True)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
