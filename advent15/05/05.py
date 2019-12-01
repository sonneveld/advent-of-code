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
    print(part2(data))



def is_nice(s):
    '''
    >>> is_nice('ugknbfddgicrmopn')
    True
    >>> is_nice('aaa')
    True
    >>> is_nice('jchzalrnumimnmhp')
    False
    >>> is_nice('haegwjzuvuyypxyu')
    False
    >>> is_nice('dvszwmarrgswjxmb')
    False
    '''
    vowel_count = sum(1 for ch in s if ch in 'aeiou')

    has_double = False
    last = None
    for ch in s:
        if ch == last:
            has_double = True
            break
        last = ch

    has_bad = False
    bad_list = "ab cd pq xy".split()
    for bad in bad_list:
        if bad in s:
            has_bad = True

    return vowel_count >= 3 and has_double and not has_bad


def part1(data):
    '''
    >>> part1(open('input.txt').read())
    255
    '''
    return sum(1 for line in data.splitlines() if is_nice(line))


def is_nice_better(s):
    '''
    >>> is_nice_better('qjhvhtzxzqqjkmpb')
    True
    >>> is_nice_better('xxyxx')
    True
    >>> is_nice_better('uurcxstgmygtbstg')
    False
    >>> is_nice_better('ieodomkazucvgmuy')
    False
    '''
    m1 = re.search(r'([a-z]{2}).*\1', s)
    m2 = re.search(r'([a-z])[a-z]\1', s)
    return m1 is not None and m2 is not None


def part2(data):
    '''
    >>> part2(open('input.txt').read())
    55
    '''
    return sum(1 for line in data.splitlines() if is_nice_better(line))



if __name__ == "__main__":
    main()
