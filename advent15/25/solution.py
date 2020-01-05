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
        row, column = ( int(x) for x in re.findall("\d+", f.read()) )
        return row,column


def num_gen(start_value=20151125):

    value = start_value
    while True:
        yield value
        value = (value * 252533) % 33554393

def part_1(data):

    row,column = data

    # figure out row offset
    row_offset = 1
    row_a = 0
    for _ in range(row):
        row_offset += row_a
        row_a += 1

    # figure out col offset
    col_offset = row_offset
    col_a = row+1
    for _ in range(column-1):
        col_offset += col_a
        col_a += 1

    for i, x in enumerate(num_gen(), 1):
        if i == col_offset:
            return x


def main():
    data = load()

    p1 = part_1(data)
    print(p1)


if __name__ == "__main__":
    main()
