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
        data = []
        for line in f:
            m = re.match(r'Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+).', line)
            assert m is not None
            data.append(  (int(m.group(2)),int(m.group(3)),int(m.group(4)),) )
        return data


def part_1(data):
    disc_len = [x[0] for x in data]
    disc_pos = [x[2] for x in data]

    # adjust to account for 1 second delay per disc
    for i in range(len(disc_pos)):
        disc_pos[i] = (disc_pos[i] + i + 1) %disc_len[i]

    for t in itertools.count():
        if disc_pos.count(disc_pos[0]) == len(disc_pos):
            return t
        disc_pos = [ (x+1)%disc_len[i] for i,x in enumerate(disc_pos) ]


def part_2(data):
    data = data + [ (11, 0, 0)]
    return part_1(data)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
