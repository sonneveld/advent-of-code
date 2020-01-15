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


DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            row = tuple(int(x) for x in re.findall(r'\-?\d+', l))
            data.append(row)
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def simulate(data):

    TOTAL_SIZE=data[-1][0]+1

    scanner_gens = [None] * TOTAL_SIZE
    scanners = [-999] * TOTAL_SIZE
    layer_sizes = [None] * TOTAL_SIZE

    scanner_locations = set()

    for layer, depth in data:
        scanner_gens[layer] = cycle(chain(range(depth), range(depth-2, 0, -1)))
        layer_sizes[layer] = depth
        scanner_locations.add(layer)

    packet = 0
    severity = 0

    for layer in scanner_locations:
        scanners[layer] = next(scanner_gens[layer])

    while packet < TOTAL_SIZE:
        # print()

        # pos_dist = [None] * TOTAL_SIZE
        # if packet >= 0 and packet < TOTAL_SIZE:
        #     pos_dist[packet] = 1
        # print('p', pos_dist)
        # print('s', scanners)

        if packet >= 0 and scanners[packet] == 0:
            severity += packet * layer_sizes[packet]

        for layer in scanner_locations:
            scanners[layer] = next(scanner_gens[layer])

        packet += 1

    return severity


def part_1(data):
    severity = simulate(data)
    return severity


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):

    # in this case, the size includes the full period of forwards and backwards to 0
    layer_sizes = {}
    scanner_locations = []
    for layer, depth in data:
        layer_sizes[layer] = len(list(chain(range(depth), range(depth-2, 0, -1))))
        scanner_locations.append(layer)

    # sort locations so shorter periods appear earlier
    scanner_locations.sort(key=lambda s: layer_sizes[s])

    for delay in count(0):
        okay = all((delay + layer) % layer_sizes[layer] != 0 for layer in scanner_locations)
        if okay:
            return delay


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
