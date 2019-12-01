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


def part1(data):
    '''
    >>> part1('abcdef')
    609043
    >>> part1('pqrstuv')
    1048970
    >>> part1('yzbqklnj')
    282749
    '''

    data = data.strip()

    for i in itertools.count():
        hd = hashlib.md5(f"{data}{i}".encode('utf-8')).hexdigest()
        if hd.startswith("0"*5):
            return i



def hashit(i, data):
    return (i, hashlib.md5(f"{data}{i}".encode('utf-8')).hexdigest())

def part2(data):
    '''
    >>> part1('yzbqklnj')
    9962624
    '''

    data = data.strip()

    # with Pool(8) as p:
    #     for i, hexdigest in p.imap(partial(hashit, data=data), itertools.count(), 1000):
    #         if hexdigest.startswith("0"*6):
    #             return i

    for i in itertools.count():
        hd = hashlib.md5(f"{data}{i}".encode('utf-8')).hexdigest()
        if hd.startswith("0"*6):
            return i


if __name__ == "__main__":
    main()
