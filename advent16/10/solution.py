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
        data = []
        for line in f:
            m = re.match(r'bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)', line)
            if m:
                bot, low_t, low_id, high_t, high_id = m.groups()
                data.append(('rule', bot, low_t, low_id, high_t, high_id))
                continue

            m = re.match(r'value (\d+) goes to bot (\d+)', line)
            if m:
                value, bot = m.groups()
                value = int(value)
                data.append(('init', bot, value))
                continue

            raise Exception(f"bad line: {line}")

        return data


def solution(data):

    output = {}
    output['0'] = 0
    output['1'] = 0
    output['2'] = 0
    bots = {}
    rules = {}
    bot_ids = set()

    for stmt in data:
        
        if stmt[0] == "init":
            bot, value = stmt[1:]
            if bot not in bots:
                bots[bot] = []
            bots[bot].append(value)
        elif stmt[0] == "rule":
            bot, low_t, low_id, high_t, high_id = stmt[1:]
            if bot not in bots:
                bots[bot] = []
            rules[bot] = (low_t, low_id, high_t, high_id)
        else:
            raise Exception(f'unknown stmt: {stmt}')

    p1_answer = None

    while any(len(x) >= 2 for x in bots.values()):

        for bot, rule in rules.items():
            
            if len(bots[bot]) < 2:
                continue

            low_t, low_id, high_t, high_id = rule

            chips = bots[bot]
            bots[bot] = []
            chips.sort()
            assert(len(chips) == 2)

            if chips == [17, 61]:
                p1_answer = bot

            if low_t == 'bot':
                assert(len(bots[low_id]) < 2)
                bots[low_id].append(chips[0])
            else:
                output[low_id] = chips[0]

            if high_t == 'bot':
                assert(len(bots[high_id]) < 2)
                bots[high_id].append(chips[1])
            else:
                output[high_id] = chips[1]

    return p1_answer,  output['0'] * output['1'] * output['2']


def main():
    data = load()

    p1, p2 = solution(data)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
