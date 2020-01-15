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
        return int(f.read())


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def part_1(data):

    buf = [0]
    skip_size = data
    i = 0
    v = 1

    while True:
        i = (i + skip_size) % len(buf)
        buf.insert(i+1, v)
        if v == 2017:
            break
        v += 1
        i = i+1

    wanted_index = buf.index(2017)
    return buf[  (wanted_index+1)% len(buf)  ]


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def generator_slow(data, last_v = 50_000_000):

    buf = [0]
    skip_size = data
    i = 0
    v = 1

    while True:
        i = (i + skip_size) % len(buf)

        if buf[i] == 0:
            yield v

        buf.insert(i+1, v)

        if v == last_v:
            break

        v += 1
        i = i+1


def generator(skip_size, last_v = 50_000_000):

    buf = deque()
    buf.appendleft(0)

    v = 1

    while True:

        buf.rotate(-(skip_size+1))

        if buf[-1] == 0:
            yield v

        buf.appendleft(v)

        if v == last_v:
            break

        v += 1



def part_2(data):

    result = None
    for x in generator(data):
        result = x

    return result


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
