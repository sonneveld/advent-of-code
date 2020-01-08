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
NOTES:

Solution here is to implement `tgl` and then run the program with
different values for register `a`

No real issues adding `tgl` instruction. Just had to be careful of
offsets outside of program.

Turns out `jnz` also accepts a register as an offset.

Because part 2 is a little slow, there's an alternative input file 
`input_optimised` which includes a slightly rewritten input using the
made up instructions `nop` and `mul`. I added `nop` to ensure previous
jump offsets were still correct.

I did a little disassembling/testing to make sure the top half of the 
program isn't affected by the `tgl` instruction later.
'''

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

TGL_MAP = {
    # 1 arg
    'inc':'dec',
    'dec':'inc',
    'tgl':'inc',
    # '*':'inc',

    # 2 arg
    'cpy':'jnz',
    'jnz':'cpy',
    # '*':'jnz',
}

def simulate(data, init_a):

    program = deepcopy(data)

    registers = [0] * 4
    registers[REG_OFFSET['a']] = init_a

    def srcval(p):
        if p in REG_OFFSET:
            return registers[REG_OFFSET[p]]
        else:
            return int(p)

    ip = 0
    while ip < len(program):
        inst = program[ip]
        op = inst[0]
        # print(ip, inst, registers)

        this_ip = ip

        # nop and mul were made up by me
        if op == "nop":
            ip += 1
        elif op == "mul":
            multiplier = srcval(inst[1])
            destr = inst[2]
            assert destr in 'abcd'
            registers[REG_OFFSET[destr]] *= multiplier
            ip += 1

        # day 11 instructions:
        elif op == "cpy":
            src = srcval(inst[1])
            destr = inst[2]
            assert destr in 'abcd'
            registers[REG_OFFSET[destr]] = src
            ip += 1
        elif op == "inc":
            r = inst[1]
            assert r in 'abcd'
            registers[REG_OFFSET[r]] += 1
            ip += 1
        elif op == "dec":
            r = inst[1]
            assert r in 'abcd'
            registers[REG_OFFSET[r]] -= 1
            ip += 1
        elif op == "jnz":
            val = srcval(inst[1])
            offset = srcval(inst[2])
            ip += offset if val != 0 else 1
        # added for day 23
        elif op == "tgl":
            offset = srcval(inst[1])
            other_ip = ip+offset
            if other_ip < len(program):
                program[other_ip][0] = TGL_MAP[program[other_ip][0]]
            ip += 1
        else:
            raise Exception(f"bad op: {op}")

        assert ip != this_ip # sanity check

    return registers[REG_OFFSET['a']]


def part_1(data):
    return simulate(data, 7)

def part_2(data):
    return simulate(data, 12)

def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
