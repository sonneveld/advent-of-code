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
        data = f.readlines()
        data = [x.strip() for x in data]
        return data


def update_position(pos, direction, distance):
    if direction == "U":
        return (pos[0], pos[1]-distance)
    elif direction == "D":
        return (pos[0], pos[1]+distance)
    elif direction == "R":
        return (pos[0]+distance, pos[1])
    elif direction == "L":
        return (pos[0]-distance, pos[1])
    else:
        raise Exception(f'bad direction: {direction}')


def part_1(data):

    '''
    1 2 3
    4 5 6
    7 8 9
    '''

    key_map = {
        (-1,-1) : 1,
        (0,-1) : 2,
        (+1,-1) : 3,

        (-1,0) : 4,
        (0,0) : 5,
        (+1,0) : 6,

        (-1,+1) : 7,
        (0,+1) : 8,
        (+1,+1) : 9,
    }

    pos = (0,0)

    result = []

    for line in data:
        for d in line:
            next_pos = update_position(pos, d, 1)
            if next_pos in key_map:
                pos = next_pos
        result.append(key_map[pos])

    return ''.join(str(x) for x in result)


def part_2(data):

    '''
        1
      2 3 4
    5 6 7 8 9
      A B C
        D
    '''

    key_map = {

        (2,-2) : 3,

        (1,-1) : 2,
        (2,-1) : 3,
        (3,-1) : 4,

        (0,0) : 5,
        (1,0) : 6,
        (2,0) : 7,
        (3,0) : 8,
        (4,0) : 9,

        (1,1) : 'A',
        (2,1) : 'B',
        (3,1) : 'C',

        (2,2) : 'D',
        
    }

    pos = (0,0)

    result = []

    for line in data:
        for d in line:
            next_pos = update_position(pos, d, 1)
            if next_pos in key_map:
                pos = next_pos
        result.append(key_map[pos])

    return ''.join(str(x) for x in result)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
