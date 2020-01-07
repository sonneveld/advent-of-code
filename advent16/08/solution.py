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

'''
 	    0	1	2	3	4	5	6	7	8	9	A	B	C	D	E	F
U+258x	▀	▁	▂	▃	▄	▅	▆	▇	█	▉	▊	▋	▌	▍	▎	▏
U+259x	▐	░	▒	▓	▔	▕	▖	▗	▘	▙	▚	▛	▜	▝	▞	▟
'''

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for line in f:

            m = re.match(r'rect (\d+)x(\d+)', line)
            if m is not None:
                data.append(('rect', int(m.group(1)), int(m.group(2))))
                continue

            m = re.match(r'rotate column x=(\d+) by (\d+)', line)
            if m is not None:
                data.append(('rotcol', int(m.group(1)), int(m.group(2))))
                continue

            m = re.match(r'rotate row y=(\d+) by (\d+)', line)
            if m is not None:
                data.append(('rotrow', int(m.group(1)), int(m.group(2))))
                continue

            raise Exception(f"bad line: {line}")

        return data

    
def dump_state(state):
    for y in range(6):
        for x in range(50):
            print("█" if state[(x,y)] else "░", end ='')
        print()


def part_1(data):

    state = {}
    for y in range(6):
        for x in range(50):
            state[(x,y)] = False

    dump_state(state)

    for cmd, a, b in data:
        print()
        print (cmd, a, b)
        if cmd == "rect":
            w,h = a,b
            for y in range(h):
                for x in range(w):
                    state[(x,y)] = True

        elif cmd == "rotcol":
            x,ammt = a,b
            new_state = dict(state)
            for y in range(6):
                new_state[(x,y)] = state[(x,(y-ammt)%6)]
            state = new_state


        elif cmd == "rotrow":
            y,ammt = a,b
            new_state = dict(state)
            for x in range(50):
                new_state[(x,y)] = state[((x-ammt)%50,y)]
            state = new_state

        else:
            raise Exception(f"bad cmd: {cmd}")

        dump_state(state)


    return list(state.values()).count(True)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)


if __name__ == "__main__":
    main()
