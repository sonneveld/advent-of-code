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
        data = f.read()
        return data


def value_gen(data):
    for i in itertools.count(0):
        b = f"{data}{i}".encode("ascii")
        h = hashlib.md5(b).hexdigest()
        if h.startswith("00000"):
            yield h[5], h[6]
    
def part_1(data):
    result = []
    for x, _ in value_gen(data):
        result.append(x)
        print (''.join(result).ljust(8, "_"))
        if len(result) == 8:
            return ''.join(result)


def part_2(data):
    result = [None] * 8

    for pos, ch in value_gen(data):
        if pos not in "01234567":
            continue
        pos = ord(pos) - ord('0')
        if result[pos] is not None:
            continue
        result[pos] = ch

        print(''.join(x if x is not None else "_" for x in result))

        if result.count(None) == 0:
            break

    return ''.join(result)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    print()
    
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
