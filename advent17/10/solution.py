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
        return f.read().strip()


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def part_1(data):

    data = [int(x) for x in re.findall(r'\-?\d+', data)]

    numbers = list(range(256))
    curpos = 0
    skipsize = 0

    for l in data:
        first = numbers[:l]
        first.reverse()
        last = numbers[l:]
        numbers = last + first
        curpos = (curpos + l) % len(numbers)

        if skipsize > 0:
            first = numbers[:skipsize]
            last = numbers[skipsize:]
            numbers = last + first
            curpos = (curpos + skipsize) % len(numbers)
        
        skipsize += 1

    first = numbers[:256 - curpos]
    last = numbers[256 - curpos:]

    numbers = last + first
    return numbers[0] * numbers[1]


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

# via https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def hashit(s):

    lengths = [ord(ch) for ch in s]
    lengths += [17, 31, 73, 47, 23]

    numbers = list(range(256))
    curpos = 0
    skipsize = 0

    for _ in range(64):
        for l in lengths:
            first = numbers[:l]
            first.reverse()
            last = numbers[l:]
            numbers = last + first
            curpos = (curpos + l) % len(numbers)

            if skipsize > 0:
                first = numbers[:skipsize]
                last = numbers[skipsize:]
                numbers = last + first
                curpos = (curpos + skipsize) % len(numbers)
            
            skipsize = (skipsize + 1) % len(numbers)

    # adjust so first element is 0
    first = numbers[:256 - curpos]
    last = numbers[256 - curpos:]
    numbers = last + first

    result = []
    for group in grouper(numbers, 16):
        v = functools.reduce(lambda x,y: x^y, group)
        result.append("%02x"%v)

    return ''.join(result)


def part_2(data):

    assert hashit('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert hashit('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    assert hashit('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert hashit('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

    return hashit(data.strip())


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
