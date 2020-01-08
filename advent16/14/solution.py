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

'''
NOTES:
I stupidly was converting the input to an int and then I wasn't even
using the right input! (I was using an input from previous day)
'''

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.read().strip()
        return data

@lru_cache(1024)
def hashit(salt, index, n=1):
    s = f"{salt}{index}"
    for _ in range(n):
        s = hashlib.md5(s.encode('ascii')).hexdigest()
    return s


triple_re = re.compile(r'([0-9a-f])\1\1')

def gen_keys(salt, stretch=1):

    for x in itertools.count():
        h = hashit(salt, x, stretch)

        m = triple_re.search(h)
        if m is None:
            continue
        ch = m.group(1)
        search_str = ch*5

        if any(True for y in range(x+1, x+1000+1) if search_str in hashit(salt,y, stretch)):
            yield x, h


def part_1(data):
    salt = data
    key_count = 1
    for key_count, v in enumerate(gen_keys(salt), 1):
        index, k = v
        print (key_count, index, k)
        if key_count == 64:
            return index


def part_2(data):
    salt = data
    key_count = 1
    for key_count, v in enumerate(gen_keys(salt, 2016+1), 1):
        index, k = v
        print (key_count, index, k)
        if key_count == 64:
            return index


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
