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
        data = f.readlines()
        data = [x.strip() for x in data]
        return data

    
def part_1(data):
    result = []
    for i in range(len(data[0])):
        counter = Counter(x[i] for x in data)
        result.append(counter.most_common(1)[0][0])
    return ''.join(result)


def part_2(data):
    result = []
    for i in range(len(data[0])):
        counter = Counter(x[i] for x in data)
        result.append(counter.most_common()[-1][0])
    return ''.join(result)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
