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
from itertools import combinations, permutations, product, count, cycle, islice
from multiprocessing import Pool
from math import sqrt


DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            l = l.strip()
            tokens = tuple(int(x) for x in l.split("/"))
            data.append(tokens)
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def needed_pins(bridge):

    pins = 0
    for b in bridge:
        if b[0] == pins:
            pins = b[1]
        else:
            pins = b[0]
    return pins

def bridge_generator(data):

    all_components = set(data)

    zeros = set()
    for c in data:
        if 0 in c:
            zeros.add(c)

    q = []
    for z in zeros:
        q.append([z,])

    while q:
        next_q = []

        for bridge in q:

            available_components = all_components - set(bridge)

            next_pins = needed_pins(bridge)

            next_components = [x for x in available_components if next_pins in x]

            if len(next_components) == 0:
                yield bridge

            for c in next_components:
                next_q.append(  bridge + [c])

        q = next_q


def bridge_strength(bridge):
    return sum(sum(x) for x in bridge)


def part_1(data):

    result = 0

    for b in bridge_generator(data):
        result = max(result, bridge_strength(b))

    return result


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):

    result = []
    result_strength = -1

    for b in bridge_generator(data):
        bs = bridge_strength(b)

        if len(b) >= len(result):

            # need to reset because there could be a stronger, shorter bridge
            if len(b) != len(result):
                result = []
                result_strength = -1

            result = b
            result_strength = max(result_strength, bs)

    return result_strength


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
