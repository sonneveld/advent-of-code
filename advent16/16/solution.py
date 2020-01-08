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
        return f.read().strip()

def dragon(s):
    return s + "0" + ''.join('1' if x == "0" else "0" for x in reversed(s))

# via https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def solution(data, LEN):

    s = data
    while len(s) < LEN:
        s = dragon(s)

    s = s[:LEN]
    assert(len(s) == LEN)
    # print(s)

    checksum = s
    while True:
        checksum = ''.join('1' if x[0]==x[1] else '0' for x in grouper(checksum, 2))
        if len(checksum) % 2 != 0:
            break

    return checksum

def part_1(data):
    return solution(data, 272)

def part_2(data):
    return solution(data, 35651584)


def main():
    data = load()

    assert dragon('1') == '100'
    assert dragon('0') == '001'
    assert dragon('11111') == '11111000000'
    assert dragon('111100001010') == '1111000010100101011110000'

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
