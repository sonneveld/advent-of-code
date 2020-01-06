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
        data = f.readlines()
        data = [x.strip() for x in data]
        return data

    
def contains_abba(s):
    result  = re.findall(r'([a-z])([a-z])\2\1', s)
    return any(x[0] != x[1] for x in result)

def supernet_sequence(s):
    return re.sub(r'\[.*?\]', '.', s)

def hypernet_sequence(s):
    return '.'.join(re.findall(r'\[(.*?)\]', s))

def part_1(data):
    result = 0
    for line in data:
        if contains_abba(supernet_sequence(line)) and not contains_abba(hypernet_sequence(line)):
            result += 1
    return result


def get_abas(s):
    # must allow overlapping
    for i in range(len(s) - 2):
        if s[i] == s[i+2] and s[i] != s[i+1]:
            yield s[i:i+3]

def invert_aba(abas):
    for aba in abas:
        yield f'{aba[1]}{aba[0]}{aba[1]}'

def part_2(data):
    result = 0
    for line in data:
        ss = supernet_sequence(line)
        hs = hypernet_sequence(line)

        ss_aba = set(get_abas(ss))
        hs_aba = set(invert_aba(get_abas(hs)))
        if ss_aba & hs_aba:
            result += 1
    return result


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
