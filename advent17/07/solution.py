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
        data = []
        for l in f:
            l = l.strip()
            tokens = re.findall(r'\w+', l)
            size = int(tokens[1])
            name = tokens[0]
            children = tokens[2:]
            data.append((name, size, children))
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def get_parent_of(data, wanted_name):
    for name, size, children in data:
        if wanted_name in children:
            return name
    return None

def get_root(data):
    for name, size, children in data:
        parent = get_parent_of(data, name)
        if parent is None:
            return name

    raise Exception("no root found")

def part_1(data):
    return get_root(data)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):

    root = get_root(data)

    nodes = {}
    for name, size, children in data:
        nodes[name] = (size, children)
    
    def get_total_size(name):
        nsize, nchildren = nodes[name]
        for cname in nchildren:
            nsize += get_total_size(cname)
        return nsize

    need = None

    n = nodes[root]
    while True:
        nsize = n[0]
        children = n[1]
        sizes = []
        for cname in children:
            sizes.append(get_total_size(cname))
        if len(set(sizes)) <= 1:
            # balanced children so we need to adjust THIS node
            return nsize + need
        
        size_counter = Counter(sizes)
        balanced_size = size_counter.most_common()[0][0]
        unbalanced_size = size_counter.most_common()[-1][0]

        if need == None:
            need = balanced_size - unbalanced_size

        unbalanced_child = children[sizes.index(unbalanced_size)]

        n = nodes[unbalanced_child]


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
