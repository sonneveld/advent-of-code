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
from itertools import combinations, permutations, product, count, cycle
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
            tokens = re.findall(r'\d+', l)
            tokens = [int(x) for x in tokens]
            data.append(tokens)
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def find_group_with(data, x):

    group = set([x])

    last_group_size = -1
    while len(group) != last_group_size:
        last_group_size = len(group)
        for row in data:
            if group & set(row):
                group |= set(row)

    return group

def part_1(data):
    return len(find_group_with(data, 0))


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):

    ungrouped_nodes = set()
    for row in data:
        ungrouped_nodes |= set(row)

    group_count = 0

    while ungrouped_nodes:
        n = ungrouped_nodes.pop()
        ng = find_group_with(data, n)
        # print(ng)
        group_count += 1
        ungrouped_nodes -= ng

    return group_count


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
