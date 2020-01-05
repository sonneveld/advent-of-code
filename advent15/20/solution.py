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

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        return int(f.read())

# via https://rosettacode.org/wiki/Factors_of_an_integer#Python
def factor(n):
    factors = set()
    for x in range(1, int(sqrt(n)) + 1):
        if n % x == 0:
            factors.add(x)
            factors.add(n//x)
    return factors

def part_1(data):

    for house in itertools.count():

        if DEBUG:
            if house % 100000 == 0:
                print(house)

        presents = 0
        for elf in factor(house):
            presents += elf * 10

        if presents >= data:
            return house


def part_2(data):

    for house in itertools.count():

        if DEBUG:
            if house % 100000 == 0:
                print(house)

        presents = 0
        for elf in factor(house):
            if house // elf <= 50 : 
                presents += elf * 11
        
        if presents >= data:
            return house


def main():
    data = load()
    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
