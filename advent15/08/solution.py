#!/usr/bin/env python3

import re
import collections
import sys
import os
import random
import doctest
import hashlib
import itertools
from multiprocessing import Pool
from heapq import heappush, heappop
from functools import lru_cache, partial


DEBUG = "DEBUG" in os.environ

def main():
    sys.setrecursionlimit(2000)

    if DEBUG:
        doctest.testmod()

    try:
        input_filename = sys.argv[1]
    except IndexError:
        input_filename = "input.txt"

    with open(input_filename) as f:
        data = f.read()

    print(part1(data))
    print(part2(data))



sample = r'''""
"abc"
"aaa\"aaa"
"\x27"'''

def part1(data):
    total = 0
    for line in data.splitlines():
        total += len(line) - len(eval(line))
    return total


def encode(s):
    def g():
        yield '"'
        for ch in s:
            if ch == '"':
                yield r'\"'
            elif ch == '\\':
                yield r'\\'
            else:
                yield ch
        yield '"'
    return ''.join(g())


def part2(data):
    '''
    >>> part2(sample)
    19
    '''
    total = 0
    for line in data.splitlines():
        # print (repr(line), len(encode(line)) , len(line))
        total += len(encode(line))  - len(line)
    return total

# NOT 1798






if __name__ == "__main__":
    main()
