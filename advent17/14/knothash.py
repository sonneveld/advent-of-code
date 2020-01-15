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

from collections import Counter, defaultdict, namedtuple, deque
from copy import copy, deepcopy
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product, count, cycle, islice, chain
from multiprocessing import Pool
from math import sqrt

# From 2017 Day 10!

# via https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def hashit_b(s):

    lengths = [ord(ch) for ch in s]
    lengths += [17, 31, 73, 47, 23]

    numbers = list(range(256))
    curpos = 0
    skipsize = 0

    for _ in range(64):
        for l in lengths:
            first = numbers[:l]
            first.reverse()
            last = numbers[l:]
            numbers = last + first
            curpos = (curpos + l) % len(numbers)

            if skipsize > 0:
                first = numbers[:skipsize]
                last = numbers[skipsize:]
                numbers = last + first
                curpos = (curpos + skipsize) % len(numbers)
            
            skipsize = (skipsize + 1) % len(numbers)

    # adjust so first element is 0
    first = numbers[:256 - curpos]
    last = numbers[256 - curpos:]
    numbers = last + first

    result = []
    for group in grouper(numbers, 16):
        v = functools.reduce(lambda x,y: x^y, group)
        result.append(v)

    return result


def hashit(s):

    result_b = hashit_b(s)

    result = []
    for b in result_b:
        result.append("%02x"%v)
    return ''.join(result)
