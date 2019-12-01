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



def parse_data(data):

    for line in data.splitlines():
        cmd = None
        if 'toggle' in line:
            cmd = 'toggle'
        elif 'turn on' in line:
            cmd = 'on'
        elif 'turn off' in line:
            cmd = 'off'
        x1,y1,x2,y2 = [int(x) for x in re.findall(r'[\-\+]?[\d]+', line)]
        assert (x1 <= x2)
        assert (y1 <= y2)
        yield (cmd, x1,y1,x2,y2)


def part1(data):
    '''
    >>> part1('turn on 0,0 through 999,999')
    1000000
    >>> part1('toggle 0,0 through 999,0')
    1000
    >>> part1('turn off 499,499 through 500,500')
    0
    '''

    lights = {}
    for cmd, x1, y1, x2, y2 in parse_data(data):
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if cmd == "on":
                    lights[ (x,y) ] = True
                elif cmd == "off":
                    lights[ (x,y) ] = False
                elif cmd == "toggle":
                    lights[ (x,y) ] = not lights.get((x,y), False)

    return sum(1 for x in lights.values() if x)




def part2(data):
    '''
    >>> part2('turn on 0,0 through 0,0')
    1
    >>> part2('toggle 0,0 through 999,999')
    2000000
    '''
    lights = {}
    for cmd, x1, y1, x2, y2 in parse_data(data):
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if cmd == "on":
                    lights[ (x,y) ] = lights.get((x,y), 0) + 1
                elif cmd == "off":
                    lights[ (x,y) ] = max(0, lights.get((x,y), 0) - 1)
                elif cmd == "toggle":
                    lights[ (x,y) ] = lights.get((x,y), 0) + 2

    return sum(lights.values())


# NOT 2440255




if __name__ == "__main__":
    main()
