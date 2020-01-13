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
            l = l.strip()
            tokens = l.split()
            op = tokens[0]
            args = [x if x in string.ascii_lowercase else int(x) for x in tokens[1:]]
            data.append( [op] + args )
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

class State():

    def __init__(self, data):
        self.data = data

        self.ip = 0
        self.registers = defaultdict(int)

        self.instruction_count = 0

        self.mul_count = 0


def simulate(state):

    def src_arg(v):
        if isinstance(v, str):
            return state.registers[v]
        else:
            return v

    def write_reg(dest, v):
        assert isinstance(dest, str)
        state.registers[dest] = v

    while state.ip < len(state.data):

        this_ip = state.ip
        instr = state.data[state.ip]
        op = instr[0]
        args = instr[1:]

        if op == "set":
            write_reg(args[0], src_arg(args[1]))
            state.ip += 1

        elif op == "sub":
            v = src_arg(args[0]) - src_arg(args[1])
            write_reg(args[0], v)
            state.ip += 1

        elif op == "mul":
            v = src_arg(args[0]) * src_arg(args[1])
            write_reg(args[0], v)
            state.ip += 1
            state.mul_count += 1

        elif op == "jnz":
            x = src_arg(args[0])
            y = src_arg(args[1])
            if x != 0:
                state.ip += y
            else:
                state.ip += 1

        else:
            raise Exception(f"bad instruction: {instr}")

        state.instruction_count += 1
        assert state.ip != this_ip

    return 'HALT'


def part_1(data):
    state = State(data)
    simulate(state)
    return state.mul_count


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2_slow(data):
    state = State(data)
    state.registers['a'] = 1
    simulate(state)
    return state['h']

'''
    The code below was hand converted from the input file.

    b = 106700
    c = 123700

    while True:

        f = 1
        d = 2

        while True:
            e = 2
            while True:
                g = (d * e) - b
                if g == 0:
                    f = 0
                e += 1
                g = e - b
                if g == 0: break

            d += 1
            g = d - b
            if g == 0: break

        if f == 0:
            h +=1

        set g b
        sub g c

        if g == 0:
            return h

        b += 17

'''

# from https://stackoverflow.com/a/17377939/84262
def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True

def part_2():
    ''' 
    Determines the number of non-primes between 106700 .. 106700+17*1000, stepping 17
    '''

    b = 106700
    c = 106700 + (17 * 1000)  # end condition
    h = 0

    for b in range(b, c+1, 17):

        '''
        prime = 1
        for d in range(2, b):
            for e in range(2, b):
                if (d * e) == b:
                    prime = 0
        '''

        prime = is_prime(b)

        if prime == 0:
            h += 1

    return h


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2()
    print(p2)


if __name__ == "__main__":
    main()
