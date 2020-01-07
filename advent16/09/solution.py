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
        return f.read()


def part_1(data):

    result = ''

    while data:
        m = re.match(r'\((\d+)x(\d+)\)|([A-Z]+)', data)
        assert m is not None
        data = data[m.end(0):]

        if m.group(3):
            # print("plain", m.group(3))
            result += m.group(3)
        else:
            numchar,repeat = int(m.group(1)), int(m.group(2))
            # print('rep', numchar,repeat)
            s = data[:numchar]
            data = data[numchar:]
            result += s * repeat

    return len(result)


def part_2(data):

    result = 0

    while data:
        m = re.match(r'\((\d+)x(\d+)\)|([A-Z]+)', data)
        assert m is not None
        data = data[m.end(0):]

        if m.group(3):
            # print("plain", m.group(3))
            result += len(m.group(3))
        else:
            numchar,repeat = int(m.group(1)), int(m.group(2))
            # print('rep', numchar,repeat)
            s = data[:numchar]
            data = data[numchar:]
            result += repeat * part_2(s)

    return result


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
