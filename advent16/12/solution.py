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
            line = line.strip()
            tokens = line.split()
            data.append(tokens)
        return data



REG_OFFSET = { 'a':0, 'b':1, 'c':2, 'd':3, }

def simulate(data, init_c = None):

    registers = [0] * 4
    if init_c is not None:
        registers[REG_OFFSET['c']] = init_c

    def srcval(p):
        if p in REG_OFFSET:
            return registers[REG_OFFSET[p]]
        else:
            return int(p)

    # count = 0

    ip = 0
    while ip < len(data):
        # count += 1
        inst = data[ip]
        op = inst[0]

        if op == "cpy":
            src,destr = inst[1:]
            src = srcval(src)
            registers[REG_OFFSET[destr]] = src
            ip += 1
        elif op == "inc":
            r = inst[1]
            registers[REG_OFFSET[r]] += 1
            ip += 1
        elif op == "dec":
            r = inst[1]
            registers[REG_OFFSET[r]] -= 1
            ip += 1
        elif op == "jnz":
            src,offset = inst[1:]
            src = srcval(src)
            offset = int(offset)
            ip += offset if src != 0 else 1
        else:
            raise Exception(f"bad op: {op}")

    # print(f'num instr: {count}')

    return registers[REG_OFFSET['a']]


def part_1(data):
    return simulate(data)

def part_2(data):
    return simulate(data, init_c=1)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
