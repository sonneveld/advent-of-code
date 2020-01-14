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

from collections import Counter, defaultdict, namedtuple
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
        a, b = [int(x) for x in re.findall(r'\d+', f.read())]
        return a,b


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def generator(start_val, factor, multiples_of=1):

    v = start_val
    while True:
        v = (v*factor) % 2147483647

        if v % multiples_of == 0:
            yield v

def part_1(data):
    a_start_val, b_start_val = data

    match_count = 0
    for a, b in itertools.islice(zip(generator(a_start_val, 16807), generator(b_start_val, 48271)), 40_000_000):
        if (a & 0xFFFF) == (b & 0xFFFF):
            match_count += 1
    return match_count


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):
    a_start_val, b_start_val = data

    match_count = 0
    for a, b in itertools.islice(zip(generator(a_start_val, 16807, 4), generator(b_start_val, 48271, 8)), 5_000_000):
        if (a & 0xFFFF) == (b & 0xFFFF):
            match_count += 1
    return match_count
    

def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
