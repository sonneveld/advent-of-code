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
        data = f.read()
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def group_score(g, nesting=1):
    if g is None:
        return 0
    return nesting + sum(group_score(x, nesting+1) for x in g)

def part_1(data):
    data = re.sub(r'\!.', '', data)
    data = re.sub(r'\<.*?\>', 'None', data)
    data = data.replace('{', '[')
    data = data.replace('}', ']')

    value = eval(data)

    return group_score(value, 1)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):
    data = re.sub(r'\!.', '', data)

    result = 0
    for garbage in re.findall(r'\<(.*?)\>', data):
        result += len(garbage)

    return result
    

def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
