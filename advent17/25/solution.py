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

from collections import Counter, defaultdict, namedtuple
from copy import copy, deepcopy
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product, count, cycle, islice
from multiprocessing import Pool
from math import sqrt


DEBUG = "DEBUG" in os.environ

'''
NOTES:

I solved this initially by converting the input into python code via
a series of regexes. It did require a little hand editing, adding
continues and elifs.

This is a more "general" solution, but a little slower.

Optimisation idea: map to a lookup table of 
    (state,value) -> (writevalue, slot_offset, new_state)
'''

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = [x.strip() for x in f.readlines()]
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def part_1(data):

    m = re.search(r'Begin in state (\w).', data[0])
    assert m is not None
    state = m.group(1)

    m = re.search(r'Perform a diagnostic checksum after (\d+) steps.', data[1])
    assert m is not None
    num_steps = int(m.group(1))
    
    tape = defaultdict(int)
    slot = 0

    for _ in range(num_steps):

        ip = data.index(f'In state {state}:')
        if tape[slot] == 0:
            ip += 2
        else:
            ip += 6
        
        m = re.search(r'- Write the value (\d+).', data[ip])
        assert m is not None
        tape[slot] = int(m.group(1))
        ip += 1

        if '- Move one slot to the left.' in data[ip]:
            slot -= 1
        elif '- Move one slot to the right.' in data[ip]:
            slot += 1
        else:
            raise Exception()
        ip += 1

        m = re.search(r'- Continue with state (\w).', data[ip])
        assert m is not None
        state = m.group(1)

    return list(tape.values()).count(1)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)



if __name__ == "__main__":
    main()
