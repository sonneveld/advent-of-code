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

from collections import Counter
from collections import defaultdict
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import product
from multiprocessing import Pool


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    result = []
    with open(filename) as f:
        data = f.readline().strip()
        data = [ord(x) - ord('a') for x in data]
        return data


def incpass(data):

    new_data = [0] * len(data)

    carry = [0] * len(data)
    carry[-1] = 1

    for i, x in reversed(list(enumerate(data))):

        x += carry[i]
        if x > 25:
            x = 0
            if i >= 0:
                carry[i-1] = 1
        new_data[i] = x
        
    return new_data


def has_inc_straight(data):

    for i,x in enumerate(data):
        if i >= len(data)-2:
            break
        if (data[i] == data[i+1]-1) and (data[i] == data[i+2]-2):
            return True
    return False


bad_letters = frozenset([ord('i')-ord('a'), ord('o')-ord('a'), ord('l')-ord('a'),])

def no_bad_letters(data):
    for b in bad_letters:
        if b in data:
            return False
    return True

def pair_count(data):
    pairs = set()

    for i,x in enumerate(data):
        if i >= len(data)-1:
            break
        if data[i] == data[i+1]:
            pairs.add(data[i])

    return len(pairs)

def str_pass(data):
    result = [chr(x + ord('a')) for x in data]
    return ''.join(result)

def psw_gen(data):

    while True:
        data = incpass(data)

        r1 = has_inc_straight(data)
        r2 = no_bad_letters(data)
        r3 = pair_count(data) >= 2

        if r1 and r2 and r3:
            yield str_pass(data)
       

def main():
    data = load()
    answer = psw_gen(data)
    print(next(answer))
    print(next(answer))


if __name__ == "__main__":
    main()
