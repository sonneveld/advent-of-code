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
        reactions = []
        molecule = None
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'(\w+) \=\> (\w+)', line)
            if m is not None:
                reactions.append( (m.group(1), m.group(2)) )
            else:
                molecule = line
        
        return molecule, reactions


# via https://stackoverflow.com/a/4665027/84262
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def part_1(data):

    molecule, reactions = data

    results = set()

    for src,dest in reactions:
        src_locs = find_all(molecule, src)

        for src_loc in src_locs:

            new_molecule = molecule[:src_loc] + molecule[src_loc:].replace(src, dest, 1)
            results.add(new_molecule)

    return len(results)

def part_2(data):
    molecule, reactions = data

    count = 0
    while True:
        for src,dest in reactions:
            count += molecule.count(dest)
            molecule = molecule.replace(dest, src)

        if molecule == "e":
            break

    return count

def main():
    data = load()
    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
