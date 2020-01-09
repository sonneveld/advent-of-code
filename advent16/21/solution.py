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
        for l in f:
            m = re.match(r'swap position (\d+) with position (\d+)', l)
            if m is not None:
                data.append(("swap_pos", int(m.group(1)),int(m.group(2)), ))
                continue

            m = re.match(r'swap letter ([a-z]) with letter ([a-z])', l)
            if m is not None:
                data.append(("swap_letter", m.group(1), m.group(2)))
                continue

            m = re.match(r'rotate left (\d+) step', l)
            if m is not None:
                data.append(("rotate_left", int(m.group(1)), None ))
                continue

            m = re.match(r'rotate right (\d+) step', l)
            if m is not None:
                data.append(("rotate_right", int(m.group(1)), None ))
                continue

            m = re.match(r'rotate based on position of letter ([a-z])', l)
            if m is not None:
                data.append(("rotate_letter", m.group(1), None ))
                continue

            m = re.match(r'reverse positions (\d+) through (\d+)', l)
            if m is not None:
                data.append(("reverse_pos", int(m.group(1)),int(m.group(2)), ))
                continue

            m = re.match(r'move position (\d+) to position (\d+)', l)
            if m is not None:
                data.append(("move", int(m.group(1)),int(m.group(2)), ))
                continue

            raise Exception(f'unknown: {l}')

        return data


def scramble(data, s):

    # s = list('abcdefgh')
    s = list(s)

    # print(''.join(f'{x}' for x in range(len(s))))
    # print(''.join(s))

    for op, arg1, arg2 in data:

        # print()
        # print(op, arg1, arg2)
        # print(''.join(s))

        if op == "swap_pos":
            a = s[arg1]
            b = s[arg2]
            s[arg1] = b
            s[arg2] = a
        elif op == "swap_letter":
            a_index = s.index(arg1)
            b_index = s.index(arg2)
            a = s[a_index]
            b = s[b_index]
            s[a_index] = b
            s[b_index] = a
        elif op == "rotate_left":
            for x in range(arg1):
                s = s[1:] + [s[0]]
        elif op == "rotate_right":
            for x in range(arg1):
                s = [s[-1]] + s[:-1] 
        elif op == "rotate_letter":
            a_index = s.index(arg1)
            rot_n = a_index + 1
            if a_index >= 4:
                rot_n += 1
            for x in range(rot_n):
                s = [s[-1]] + s[:-1] 
        elif op == "reverse_pos":
            a_index = arg1
            b_index = arg2
            s = s[0:a_index] + list(reversed(s[a_index:b_index+1])) +  s[b_index+1:]
        elif op == "move":
            ch = s.pop(arg1)
            s = s[:arg2] + [ch] + s[arg2:]
        else:
            raise Exception(f"bad op: {op}")

    #     print(''.join(f'{x}' for x in range(len(s))))
    #     print(''.join(s))
    
    # print(''.join(s))

    return ''.join(s)


def part_1(data):
    return scramble(data, 'abcdefgh')

def part_2(data):
    WANTED = 'fbgdceah'
    for s in permutations('abcdefgh'):
        scrambled = scramble(data, s)
        if scrambled == WANTED:
            return ''.join(s)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
