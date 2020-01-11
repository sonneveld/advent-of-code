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

from copy import copy, deepcopy

DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            l = l.strip()
            data.append(l.split())
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def part_1(data):

    count = 0
    for row in data:
        c = Counter(row)
        list_of_one = c.most_common(1)
        phrase, num = list_of_one[0]
        if num == 1:
            count += 1

    return count


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):
    count = 0
    for row in data:
        row = [''.join(sorted(x)) for x in row]
        c = Counter(row)
        list_of_one = c.most_common(1)
        phrase, num = list_of_one[0]
        if num == 1:
            count += 1

    return count


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
