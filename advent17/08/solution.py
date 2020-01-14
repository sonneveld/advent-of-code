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

from copy import copy, deepcopy

DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            m = re.match(r'(\w+) (inc|dec) (\-?\d+) if (\w+) ([!<>=]+) (\-?\d+)', l)
            if not m:
                raise Exception(f'bad line: {l}')
            stmt_reg, stmt_op, stmt_val, exp_reg, exp_op, exp_val = m.groups()
            stmt_val = int(stmt_val)
            exp_val = int(exp_val)
            data.append((stmt_reg, stmt_op, stmt_val, exp_reg, exp_op, exp_val))
        return data


def solution(data):
    registers = defaultdict(int)

    max_any_value = 0

    for stmt_reg, stmt_op, stmt_val, exp_reg, exp_op, exp_val in data:

        # print( stmt_reg, stmt_op, stmt_val, 'if', exp_reg, exp_op, exp_val, registers)

        do_stmt = False
        if exp_op == "==":
            do_stmt = registers[exp_reg] == exp_val
        elif exp_op == "!=":
            do_stmt = registers[exp_reg] != exp_val
        elif exp_op == "<":
            do_stmt = registers[exp_reg] < exp_val
        elif exp_op == "<=":
            do_stmt = registers[exp_reg] <= exp_val
        elif exp_op == ">":
            do_stmt = registers[exp_reg] > exp_val
        elif exp_op == ">=":
            do_stmt = registers[exp_reg] >= exp_val
        else:
            raise Exception(f'bad op: {exp_op}')

        if not do_stmt:
            continue

        # print("   DO!", stmt_reg, stmt_op, stmt_val)

        if stmt_op == "inc":
            registers[stmt_reg] += stmt_val
        elif stmt_op == "dec":
            registers[stmt_reg] -= stmt_val
        else:
            raise Exception(f'bad op: {stmt_op}')

        max_any_value = max(max_any_value, registers[stmt_reg])

    return max(registers.values()), max_any_value


def main():
    data = load()

    p1, p2 = solution(data)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
