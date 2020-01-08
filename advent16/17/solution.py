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


def adjust_pos(pos, direction):
    if direction == "U":
        return (pos[0], pos[1]-1)
    elif direction == "D":
        return (pos[0], pos[1]+1)
    elif direction == "L":
        return (pos[0]-1, pos[1])
    elif direction == "R":
        return (pos[0]+1, pos[1])
    else:
        raise Exception(f"bad dir:{direction}")

def get_doors(data, path):
    h = hashlib.md5((data+path).encode('ascii')).hexdigest()
    doors_open = [x in 'bcdef' for x in h[:4]]
    return [x[1] for x in zip(doors_open, "UDLR") if x[0]]

def path_generator(data):

    q = []
    init_pos = (0,0)
    init_path = ''
    q.append( (init_pos, init_path) )

    while q:
        pos,path = q.pop(0)

        if pos == (3,3):
            yield path
            continue

        for direction in get_doors(data, path):
            next_pos = adjust_pos(pos, direction)
            if next_pos[0] not in (0,1,2,3):
                continue
            if next_pos[1] not in (0,1,2,3):
                continue
            next_path = path + direction
            q.append( (next_pos, next_path))


def part_1(data):
    for path in path_generator(data):
        return path

def part_2(data):

    result = 0
    for path in path_generator(data):

        new_result = len(path)
        if new_result > result:
            result = new_result

    return result


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
