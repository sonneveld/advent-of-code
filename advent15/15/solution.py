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
        result = {}
        for line in f:
            m = re.match(r"(\w+): capacity (\-?\d+), durability (\-?\d+), flavor (\-?\d+), texture (\-?\d+), calories (\-?\d+)", line)
            assert m is not None
            name, capacity, durability, flavor, texture, calories = m.groups()
            capacity, durability, flavor, texture, calories = (int(x) for x in (capacity, durability, flavor, texture, calories))
                
            result[name] = (name, capacity, durability, flavor, texture, calories)
        return result


def iter_ammts(n):
    for x in product(range(0, 101), repeat=n):
        if sum(x) == 100:
            yield x

    
def part_1(data):

    ingreds = list(data.keys())

    scores = set()

    for ammts in iter_ammts(len(ingreds)):

        tot_c = 0
        tot_d = 0
        tot_f = 0
        tot_t = 0

        for i, ammt in enumerate(ammts):

            _, capacity, durability, flavor, texture, _ = data[ingreds[i]]

            tot_c += ammt * capacity
            tot_d += ammt * durability
            tot_f += ammt * flavor
            tot_t += ammt * texture

        if tot_c <= 0: continue
        if tot_d <= 0: continue
        if tot_f <= 0: continue
        if tot_t <= 0: continue

        score = tot_c * tot_d * tot_f * tot_t
        scores.add(score)

    return max(scores)


def part_2(data):

    ingreds = list(data.keys())

    scores = set()

    for ammts in iter_ammts(len(ingreds)):

        tot_c = 0
        tot_d = 0
        tot_f = 0
        tot_t = 0
        tot_cal = 0

        for i, ammt in enumerate(ammts):

            _, capacity, durability, flavor, texture, calories = data[ingreds[i]]

            tot_c += ammt * capacity
            tot_d += ammt * durability
            tot_f += ammt * flavor
            tot_t += ammt * texture

            tot_cal += ammt * calories

        if tot_cal != 500: continue

        if tot_c <= 0: continue
        if tot_d <= 0: continue
        if tot_f <= 0: continue
        if tot_t <= 0: continue

        score = tot_c * tot_d * tot_f * tot_t
        scores.add(score)

    return max(scores)


def main():
    data = load()
    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
