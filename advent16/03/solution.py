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
        data = []
        for line in f:
            row = tuple(int(x) for x in re.findall(r'\d+', line))
            data.append(row)
        return data


def is_valid_triangle(lengths):
    return all( (t[0] + t[1]) > t[2] for t in permutations(lengths) )

def part_1(data):

    possible = 0
    for row in data:
        if is_valid_triangle(row):
            possible += 1

    return possible


# via https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def part_2(data):

    assert(len(data) % 3 == 0)

    fdata = [x[0] for x in data] + [x[1] for x in data]+ [x[2] for x in data]

    possible = 0
    for row in grouper(fdata, 3):
        if is_valid_triangle(row):
            possible += 1

    return possible



def main():
    data = load()

    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
