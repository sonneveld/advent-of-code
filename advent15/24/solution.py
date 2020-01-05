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
        return { int(x) for x in re.findall("\d+", f.read()) }



def group_comb(packages, wanted_size):
    for n in range(1, len(packages)+1):
        for x in combinations(packages, n):
            if sum(x) == wanted_size:
                yield x

def part_1(data):

    data = list(data)
    data.sort(reverse=True)

    assert sum(data) % 3 == 0
    group_size = sum(data) // 3

    result = (99999, 0)

    for x in group_comb(data, group_size):
        next_res = len(x), functools.reduce(lambda x,y: x*y, x)
        if next_res < result:
            result = next_res

    return result[1]


def part_2(data):

    data = list(data)
    data.sort(reverse=True)

    assert sum(data) % 4 == 0
    group_size = sum(data) // 4
    
    result = (99999, 0)

    for x in group_comb(data, group_size):
        next_res = len(x), functools.reduce(lambda x,y: x*y, x)
        if next_res < result:
            result = next_res

    return result[1]


def main():
    data = load()

    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
