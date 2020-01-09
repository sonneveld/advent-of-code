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
        data = []
        for l in f:
            l = l.strip()
            tokens = tuple(int(x) for x in l.split('-'))
            data.append(tokens)
        return data


def part_1(data):
    
    ranges = list(data)
    ranges.sort()

    # you never know!
    if ranges[0][0] != 0:
        return 0

    low, high = ranges[0]

    for o_low, o_high in ranges[1:]:
        # overlap
        if o_low >= low and o_low <= high:
            if o_high > high:
                high = o_high
        # adjacent
        elif o_low == high+1:
            if o_high > high:
                high = o_high
        else:
            break
    
    return high+1


def part_2(data):
    ranges = list(data)
    ranges.sort()

    result = []

    while ranges:

        low,high = ranges.pop(0)

        while ranges:
            next_low,next_high = ranges[0]
            if (next_low >= low and next_low <= high) or next_low == high+1:
                high = max(high, next_high)
                ranges.pop(0)
            else:
                break

        result.append((low,high))

    used = 0
    for l,h in result:
        used += (h-l+1)

    return 4294967296 - used


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
