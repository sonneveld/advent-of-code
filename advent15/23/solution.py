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
        result = []
        for l in f:
            l = l.strip()
            tokens = re.split(r'[\s,]+', l)
            result.append(tokens)
        return result


def simulator(data, initial_a):

    registers={}
    registers['a'] = initial_a
    registers['b'] = 0
    ip = 0

    while ip < len(data):

        instr = data[ip]
        op = instr[0]
        if DEBUG:
            print(ip, instr, "\t\t", registers)

        if op == "hlf":
            r = instr[1]
            registers[r] = registers[r] // 2
            ip += 1
        elif op == "tpl":
            r = instr[1]
            registers[r] = registers[r] * 3
            ip += 1
        elif op == "inc":
            r = instr[1]
            registers[r] += 1
            ip += 1
        elif op == "jmp":
            offset = int(instr[1])
            ip += offset
        elif op == "jie":
            r = instr[1]
            offset = int(instr[2])
            if registers[r] % 2 == 0:
                ip += offset
            else:
                ip += 1
        elif op == "jio":
            r = instr[1]
            offset = int(instr[2])
            if registers[r] == 1:
                ip += offset
            else:
                ip += 1
        else:
            raise Exception(f"bad op {op}")

    return registers['b']

def main():
    data = load()

    p1 = simulator(data, 0)
    print(p1)
    p2 = simulator(data, 1)
    print(p2)


if __name__ == "__main__":
    main()
