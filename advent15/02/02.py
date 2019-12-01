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



def calc_wrapping_paper_area(l,w,h):
    return 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)

def part1(data):
    '''
    >>> part1('2x3x4')
    58
    >>> part1('1x1x10')
    43
    >>> part1(open('input.txt').read())
    1586300
    '''
    total = 0
    for line in data.splitlines():
        l,w,h =  [int(x) for x in re.findall(r'[\-\+]?[\d]+', line)]
        total += calc_wrapping_paper_area(l,w,h)
    return total


def calc_ribbon_length(l,w,h):
    return min(2*l+2*w, 2*l+2*h, 2*w+2*h) + (l*w*h)

def part2(data):
    '''
    >>> part2('2x3x4')
    34
    >>> part2('1x1x10')
    14
    >>> part2(open('input.txt').read())
    3737498
    '''
    total = 0
    for line in data.splitlines():
        l,w,h =  [int(x) for x in re.findall(r'[\-\+]?[\d]+', line)]
        total += calc_ribbon_length(l,w,h)
    return total


if __name__ == "__main__":
    main()
