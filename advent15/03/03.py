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
    >>> part1('>')
    2
    >>> part1('^>v<')
    4
    >>> part1('^v^v^v^v^v')
    2
    >>> part1(open('input.txt').read())
    2081
    '''
    houses = set()
    x = 0
    y = 0
    houses.add( (x,y) )
    for ch in data:
        if ch == ">":
            x += 1
        if ch == "<":
            x -= 1
        if ch == "^":
            y -= 1
        if ch == "v":
            y += 1
        houses.add( (x,y) )
    return len(houses)



def update_pos(x, y, ch):
    if ch == ">":
        x += 1
    if ch == "<":
        x -= 1
    if ch == "^":
        y -= 1
    if ch == "v":
        y += 1
    return x, y


def part2(data):
    '''
    >>> part2('^v')
    3
    >>> part2('^>v<')
    3
    >>> part2('^v^v^v^v^v')
    11
    >>> part2(open('input.txt').read())
    2341
    '''
    data = list(data)
    houses = set()
    x = 0
    y = 0
    rx = 0
    ry = 0
    houses.add( (x,y) )
    while data:
        ch = data.pop(0)
        x,y = update_pos(x, y, ch)
        houses.add( (x,y) )
        if not data:
            break
        ch = data.pop(0)
        rx,ry = update_pos(rx, ry, ch)
        houses.add( (rx,ry) )
    return len(houses)


if __name__ == "__main__":
    main()
