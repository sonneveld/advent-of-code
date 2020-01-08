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
        return f.read().strip()


def solution(row, num_rows):

    result = 0

    for _ in range(num_rows):
        # print(row)
        result += row.count(".")

        next_row = []
        for i,_ in enumerate(row):
            left = '.'
            if i-1 >= 0:
                left = row[i-1]
            center = row[i]
            right = '.'
            if i+1 < len(row):
                right = row[i+1]

            v = '.'
            if (left,center,right) == ('^', '^', '.'):
                v = '^'
            elif (left,center,right) == ('.', '^', '^'):
                v = '^'
            elif (left,center,right) == ('^', '.', '.'):
                v = '^'
            elif (left,center,right) == ('.', '.', '^'):
                v = '^'

            next_row.append(v)
        
        row = ''.join(next_row)

    return result


def part_1(data):
    return solution(data, 40)

def part_2(data):
    return solution(data, 400_000)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
