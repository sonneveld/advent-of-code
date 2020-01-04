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


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        result = []
        for line in f:
            sue = dict( ( x[0], int(x[1])) for x in re.findall(r'(\w+): (\d+)', line) )
            result.append(sue)
        return result



ACTUAL_SUE = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''

def part_1(data):

    actual_sue = (x.split(": ") for x in ACTUAL_SUE.splitlines() )
    actual_sue = dict( (x[0], int(x[1])) for x in actual_sue )

    print('wanted:', actual_sue)

    for i, sue in enumerate(data, 1):

        found = True
        for k,v in sue.items():
            if k not in actual_sue:
                continue
            if actual_sue[k] != sue[k]:
                found = False
                break

        if found:
            print("got:", sue)
            return i


def part_2(data):

    GT = 'cats trees'
    LT = 'pomeranians goldfish'

    actual_sue = (x.split(": ") for x in ACTUAL_SUE.splitlines() )
    actual_sue = dict( (x[0], int(x[1])) for x in actual_sue )

    print('wanted:', actual_sue)

    for i, sue in enumerate(data, 1):

        found = True
        for k,v in sue.items():
            if k not in actual_sue:
                continue
            if k in GT:
                if sue[k] <= actual_sue[k]:
                    found = False
                    break
            elif k in LT:
                if sue[k] >= actual_sue[k]:
                    found = False
                    break
            elif actual_sue[k] != sue[k]:
                found = False
                break

        if found:
            print("got:", sue)
            return i



def main():
    data = load()
    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
