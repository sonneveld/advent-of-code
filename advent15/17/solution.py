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


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        result = [int(x.strip()) for x in f.readlines()]
        return result


def combos(data):
    for n in range(1, len(data)):
        for x in combinations(data, n):
            yield x

def part_1(data):

    result = 0
    for x in combos(data):
        if sum(x) == 150:
            result += 1

    return result
    

def part_2(data):

    num_containers = set()
    for x in combos(data):
        if sum(x) == 150:
            num_containers.add(len(x))

    num_containers = min(num_containers)

    result = 0
    for x in combos(data):
        if len(x) == num_containers and sum(x) == 150:
            result += 1

    return result


def main():
    data = load()
    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
