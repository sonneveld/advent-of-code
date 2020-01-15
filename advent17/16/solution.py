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
        return f.read().strip().split(",")


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def dance(data, programs):
    programs = list(programs)
    for x in data:
        if x[0] == 's':
            v = int(x[1:])
            second = programs[-v:]
            first = programs[:-v]
            programs = second + first
        elif x[0] == 'x':
            i0, i1 = [int(y) for y in x[1:].split("/")]
            assert i0 < len(programs)
            assert i1 < len(programs)
            p0 = programs[i0]
            p1 = programs[i1]
            programs[i0] = p1
            programs[i1] = p0
        elif x[0] == 'p':
            p0, p1 = x[1:].split("/")
            assert p0 in programs
            assert p1 in programs
            i0 = programs.index(p0)
            i1 = programs.index(p1)
            programs[i0] = p1
            programs[i1] = p0
    return programs


def part_1(data):
    programs = list('abcdefghijklmnop')
    programs = dance(data, programs)
    return ''.join(programs)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def dance_generator(data, programs):
    while True:
        programs = dance(data, programs)
        yield ''.join(programs)

def find_period(g):
    first = next(g)
    for i, x in enumerate(g,1):
        if x == first:
            return i

def part_2(data):
    programs = list('abcdefghijklmnop')

    period = find_period(dance_generator(data, programs))
    remaining = 1_000_000_000 % period

    for i in range(remaining):
        programs = dance(data, programs)

    return ''.join(programs)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
