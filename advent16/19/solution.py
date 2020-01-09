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
        return int(f.read())


def part_1(data):
    num_elves = data

    state = [1] * num_elves
    index = 0
    while True:

        # find the next elf with presents
        while state[index] == 0:
            index = (index + 1)%num_elves

        left = (index + 1)%num_elves
        while state[left] == 0:
            left = (left + 1)%num_elves

        # congratulations, you found yourself
        if index == left:
            break

        state[index] += state[left]
        state[left] = 0

        index = (left + 1)%num_elves
    
    # 0 based index
    elf = index + 1
    return elf

def part_2(data):
    num_elves = data
    state = [1] * num_elves

    elves = list(range(0, num_elves))

    elf_index = 0
    while len(elves) > 1:
        elf = elves[elf_index]
        # print('e', elf+1, [x+1 for x in elves])
        assert state[elf] != 0
        across_index = (elf_index + len(elves)//2 ) % len(elves)
        across = elves[across_index]
        # print('  across', across+1)

        if across == elf:
            break

        assert state[across] != 0

        state[elf] += state[across]
        state[across] = 0
        del elves[across_index]
        if elf_index > across_index:
            elf_index -= 1

        elf_index = (elf_index + 1) % len(elves)

    # 0 based index
    return elves[0] + 1


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
