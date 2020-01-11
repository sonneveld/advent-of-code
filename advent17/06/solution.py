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
        data = [int(x) for x in re.findall(r'\d+', f.read())]
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def routine(data):
    banks = list(data)

    while True:

        largest = max(banks)
        
        l_index = banks.index(largest)
        banks[l_index] = 0

        i = (l_index + 1)%len(banks)
        v = largest
        while v:
            banks[i] += 1
            v -= 1
            i = (i + 1)%len(banks)

        yield tuple(banks)
        

def part_1(data):

    seen = set()
    for cycles, banks in enumerate(routine(data),1):
        if banks in seen:
            return cycles
        seen.add(banks)

    return


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):
    seen = set()
    for cycles, banks in enumerate(routine(data),1):
        if banks in seen:
            break
        seen.add(banks)

    wanted_banks = banks

    for cycles, banks in enumerate(routine(wanted_banks), 1):
        if banks == wanted_banks:
            return cycles


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
