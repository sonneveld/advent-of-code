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
        result = f.readlines()
        result = [x.strip() for x in result]
        return result



def get_adj_pos(pos):

    return (
        (pos[0]-1, pos[1]-1),
        (pos[0]-1, pos[1]),
        (pos[0]-1, pos[1]+1),

        (pos[0], pos[1]-1),
        (pos[0], pos[1]+1),

        (pos[0]+1, pos[1]-1),
        (pos[0]+1, pos[1]),
        (pos[0]+1, pos[1]+1),
    )

def part_1(data):

    state = {}
    for y,row in enumerate(data):
        for x, v in enumerate(row):
            state[x,y] = True if v == "#" else False

    for t in range(100):

        new_state = {}

        for k,v in state.items():
            
            adj_pos = get_adj_pos(k)
            count = 0
            for a in adj_pos:
                if a not in state:
                    continue
                if state[a]:
                    count += 1

            if v:
                if count not in (2,3):
                    v = False
            else:
                if count == 3:
                    v = True

            new_state[k] = v

        state = new_state

    result = list(state.values()).count(True)

    return result


def part_2(data):

    state = {}
    for y,row in enumerate(data):
        for x, v in enumerate(row):
            state[x,y] = True if v == "#" else False

    min_x = min(p[0] for p in state.keys())
    max_x = max(p[0] for p in state.keys())
    min_y = min(p[1] for p in state.keys())
    max_y = max(p[1] for p in state.keys())

    def broken_lights(s):
        s[min_x, min_y] = True
        s[min_x, max_y] = True
        s[max_x, min_y] = True
        s[max_x, max_y] = True

    broken_lights(state)

    for t in range(100):

        new_state = {}

        for k,v in state.items():
            
            adj_pos = get_adj_pos(k)
            count = 0
            for a in adj_pos:
                if a not in state:
                    continue
                if state[a]:
                    count += 1

            if v:
                if count not in (2,3):
                    v = False
            else:
                if count == 3:
                    v = True

            new_state[k] = v

        broken_lights(new_state)

        state = new_state

    result = list(state.values()).count(True)

    return result



def main():
    data = load()
    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
