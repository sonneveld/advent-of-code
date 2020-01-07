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
        data = {}
        for floor, line in enumerate(f, 1):
            items = set()
            for i in re.findall(r'(\w+)( generator|\-compatible microchip)', line):
                t = 'G' if 'generator' in i[1] else 'M'
                n = i[0][0].upper()
                items.add(f'{n}{t}')
            data[floor] = items
        return data


class Building():

    def __init__(self, data):
        self.elevator = 1
        self.floors = data
        self.steps = 0
        
    def makekey(self):
        return (self.elevator, frozenset(self.floors[1]), frozenset(self.floors[2]) ,frozenset(self.floors[3]),frozenset(self.floors[4]) )

    def available_items(self):
        return self.floors[self.elevator]

    def apply(self, next_floor, with_items):
        if next_floor not in (1,2,3,4):
            return False

        assert(with_items & self.available_items() == with_items)

        prev_elevator = self.elevator

        self.floors[self.elevator] -= with_items
        self.elevator = next_floor
        self.floors[self.elevator] |= with_items

        for floor in (prev_elevator, self.elevator):
            gens = [x for x in self.floors[floor] if x[1] == 'G']
            if len(gens) > 0:
                for m in (x for x in self.floors[floor] if x[1] == 'M'):
                    if f'{m[0]}G' not in gens:
                        return False

        self.steps += 1

        return True

    def dump(self):
        all_items = set()
        for x in self.floors.values():
            all_items |= x
        for floor in range(4, 0, -1):
            print(f"F{floor}", end =' ')
            if self.elevator == floor:
                print(f"E", end ='  ')
            else:
                print(f".", end ='  ')
            
            for i in sorted(all_items):
                if i in self.floors[floor]:
                    print(i, end=" ")
                else:
                    print(". ", end = " ")
            print()


def groups_set(items):
    result = set()
    for n in range(2):
        for g in combinations(items, n+1):
            result.add(frozenset(g))
    return result

def solution(data):

    all_items = set()
    for x in data.values():
        all_items |= x

    queue = []
    states = {}
    b = Building(data)

    queue.append(b)
    states[b.makekey()] = b

    # b.dump()

    while queue:
        # print(len(queue))

        next_queue = []
        for b in queue:
            if len(b.floors[4]) == len(all_items):
                return b.steps

            next_floors = [b.elevator-1, b.elevator+1]
            groups = groups_set(b.available_items())

            for f, g in product(next_floors, groups):
                if f not in (1,2,3,4):
                    continue
                next_b = deepcopy(b)
                if not next_b.apply(f, g):
                    continue

                k = next_b.makekey()
                if k in states and next_b.steps >= states[k].steps:
                    continue

                states[k] = next_b
                next_queue.append(next_b)

        queue = next_queue


def part_1(data):
    return solution(data)

def part_2(data):
    data = deepcopy(data)
    data[1].add("DG")
    data[1].add("DM")
    data[1].add("EG")
    data[1].add("EM")
    return solution(data)

def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
