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

def simulate(data, init_a):

    registers = [0] * 4
    registers[REG_OFFSET['a']] = init_a

    def srcval(p):
        if p in REG_OFFSET:
            return registers[REG_OFFSET[p]]
        else:
            return int(p)

    ip = 0
    while ip < len(data):
        inst = data[ip]
        op = inst[0]
        # print(ip, inst, registers)

        this_ip = ip

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
        elif op == "out":
            src = inst[1]
            src = srcval(src)
            yield src
            ip += 1
        else:
            raise Exception(f"bad op: {op}")

        assert ip != this_ip # sanity check


# decompiled version, probably only for this input
# turns out it's a bit shifter
def simulate_decompiled(_, n):
    start_val = n + 365*7  # other inputs were roughly around 2550 i.e 643*4 or 170*15 or 2532

    a = start_val
    while True:
        a, c = divmod(a, 2)
        yield c

        if a == 0: 
            a = start_val


def part_1(data):

    WANTED = [0,1]*10

    for n in itertools.count():

        result = list(itertools.islice(simulate(data, n), len(WANTED)))
        # result = list(itertools.islice(simulate_decompiled(data, n), len(WANTED)))

        if result == WANTED:
            return n


def main():
    data = load()

    p1 = part_1(data)
    print(p1)


if __name__ == "__main__":
    main()
