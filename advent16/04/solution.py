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
        data = []
        for line in f:
            m = re.match('([a-z\-]+)-(\d+)\[([a-z]+)\]', line)
            name, sector, checksum = m.groups()
            sector = int(sector)
            data.append((name, sector, checksum))
        return data


def calc_checksum(name):
    result = Counter(name)
    if '-' in result:
        del result['-']
    result = list(result.items())
    result.sort(key=lambda x: x[0])
    result.sort(key=lambda x: x[1], reverse=True)
    result = result[:5]
    result = ''.join(x[0] for x in result)
    return result
    
def part_1(data):

    result = 0
    for name, sector, checksum in data:
        chk = calc_checksum(name)
        if checksum == chk:
            # print (name, sector, checksum)
            result += sector

    return result


def decrypt(name, offset):

    result = []
    for ch in name:
        if ch in string.ascii_lowercase:
            ch = ord(ch) - ord('a')
            ch = (ch + offset) % 26
            ch = chr(ch + ord('a'))
        result.append(ch)
    return ''.join(result)

def part_2(data):

    for name, sector, checksum in data:
        chk = calc_checksum(name)
        if checksum != chk:
            continue
        name = decrypt(name, sector)
        # print (name, sector)
        if name == 'northpole-object-storage':
            return sector

    raise Exception("not found")


def main():
    data = load()

    p1 = part_1(data)
    print(p1)
    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
