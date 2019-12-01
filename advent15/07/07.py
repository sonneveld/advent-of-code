#!/usr/bin/env python3

import re
import collections
import sys
import os
from heapq import heappush, heappop
from functools import lru_cache, partial
import random
import doctest
import hashlib
from multiprocessing import Pool
import itertools


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
    # print(part2(data))




op_map = {
    "AND": "&",
    "OR": "|",
    "LSHIFT": "<<",
    "RSHIFT": ">>",
}

def input_map(v):
    if v.isdigit():
        return v
    return f'wire_{v}()'

def part1(data):


    for line in data.splitlines():
        m = re.match(r'^(\w+) -> (\w+)', line)
        if m is not None:
            a, c = m.groups()
            a = input_map(a)
            exec(f'''
@lru_cache(None)
def wire_{c}():
    print('wire_{c}')
    return {a}
            ''',  globals() )
            continue

        m = re.match(r'^(\w+) (\w+) (\w+) -> (\w+)', line)
        if m is not None:
            a, op, b, c = m.groups()
            a = input_map(a)
            op = op_map[op]
            b = input_map(b)
            exec(f'''
@lru_cache(None)
def wire_{c}():
    print('wire_{c}')
    return {a} {op} {b}
            ''',  globals() )
            continue

        m = re.match(r'^NOT (\w+) -> (\w+)', line)
        if m is not None:
            a, c = m.groups()
            a = input_map(a)
            b = input_map(b)
            exec(f'''
@lru_cache(None)
def wire_{c}():
    print('wire_{c}')
    return ~ {a}
            ''',  globals() )
            continue

#             exec(f'''
# @lru_cache(None)
#     def wire_b():
#         return 956
#             ''',  globals() )

    return wire_a()







if __name__ == "__main__":
    main()
