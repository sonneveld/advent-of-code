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

def broken_simulate(data):

    ip = 0
    played_sound = None
    registers = defaultdict(int)

    sounds_played = []

    while ip < len(data):

        this_ip = ip
        instr = data[ip]
        op = instr[0]
        args = instr[1:]

        def src_arg(v):
            if isinstance(v, str):
                return registers[v]
            else:
                return v

        def write_reg(dest, v):
            assert isinstance(dest, str)
            registers[dest] = v


        if op == "snd":
            val = src_arg(args[0])
            sounds_played.append(val)
            ip += 1

        elif op == "set":
            write_reg(args[0], src_arg(args[1]))
            ip += 1

        elif op == "add":
            v = src_arg(args[0]) + src_arg(args[1])
            write_reg(args[0], v)
            ip += 1

        elif op == "mul":
            v = src_arg(args[0]) * src_arg(args[1])
            write_reg(args[0], v)
            ip += 1

        elif op == "mod":
            v = src_arg(args[0]) % src_arg(args[1])
            write_reg(args[0], v)
            ip += 1

        elif op == "rcv":
            v = src_arg(args[0])
            ip += 1
            if v != 0:
                return sounds_played[-1]
            
        elif op == "jgz":
            x = src_arg(args[0])
            y = src_arg(args[1])
            if x > 0:
                ip += y
            else:
                ip += 1

        else:
            raise Exception(f"bad instruction: {instr}")

        assert ip != this_ip


def part_1(data):
    return broken_simulate(data)


# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

class State():

    def __init__(self, data, progid, inbuf, outbuf):
        self.data = data
        self.progid = progid
        self.inbuf = inbuf
        self.outbuf = outbuf

        self.ip = 0
        self.registers = defaultdict(int)
        self.registers['p'] = progid

        self.send_count = 0
        self.instruction_count = 0


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

        if DEBUG:
            print(state.progid, "->", state.ip, instr, 'inbuf:', len(state.inbuf), 'regs:', dict(state.registers))

        if op == "snd":
            val = src_arg(args[0])
            state.outbuf.append(val)
            state.ip += 1
            state.send_count += 1
            return "SEND"

        elif op == "set":
            write_reg(args[0], src_arg(args[1]))
            state.ip += 1

        elif op == "add":
            v = src_arg(args[0]) + src_arg(args[1])
            write_reg(args[0], v)
            state.ip += 1

        elif op == "mul":
            v = src_arg(args[0]) * src_arg(args[1])
            write_reg(args[0], v)
            state.ip += 1

        elif op == "mod":
            v = src_arg(args[0]) % src_arg(args[1])
            write_reg(args[0], v)
            state.ip += 1

        elif op == "rcv":
            if len(state.inbuf) <= 0:
                return 'STALLED'
            v = state.inbuf.pop(0)
            write_reg(args[0], v)    
            state.ip += 1
            
        elif op == "jgz":
            x = src_arg(args[0])
            y = src_arg(args[1])
            if x > 0:
                state.ip += y
            else:
                state.ip += 1

        else:
            raise Exception(f"bad instruction: {instr}")

        state.instruction_count += 1
        assert state.ip != this_ip

    return 'HALT'


def part_2(data):

    p0_buf = []
    p1_buf = []

    p0 = State(data, 0, p0_buf, p1_buf)
    p1 = State(data, 1, p1_buf, p0_buf)

    while True:

        p0_instr_count = p0.instruction_count
        ret = simulate(p0)
        p0_stalled = ret == 'STALLED'

        p1_instr_count = p1.instruction_count
        ret = simulate(p1)
        p1_stalled = ret == 'STALLED'

        if p0_stalled and p1_stalled and len(p0_buf) == 0 and len(p1_buf) == 0:
            break

    return p1.send_count


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
