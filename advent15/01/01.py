#!/usr/bin/env python3

import re
import collections
import sys
import os
from heapq import heappush, heappop
from functools import lru_cache
import random
import doctest

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


def part1(data):
    '''
    >>> part1('(())')
    0
    >>> part1('()()')
    0
    >>> part1('(((')
    3
    >>> part1('(()(()(')
    3
    >>> part1('))((((( ')
    3
    >>> part1('())')
    -1
    >>> part1(' ))( ')
    -1
    >>> part1(')))')
    -3
    >>> part1(' )())()) ')
    -3
    >>> part1(open('input.txt').read())
    280
    '''
    return data.count('(') - data.count(')')

def part2(data):
    '''
    >>> part2(')')
    1
    >>> part2('()())')
    5
    >>> part2(open('input.txt').read())
    1797
    '''
    pos = 0
    for i, ch in enumerate(data):
        ch_pos = i+1
        if ch == ')':
            pos -= 1
        if ch == '(':
            pos += 1
        if pos == -1:
            return ch_pos
    return None


if __name__ == "__main__":
    main()
