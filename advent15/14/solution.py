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

from collections import Counter
from collections import defaultdict
from collections import namedtuple
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import permutations
from itertools import product
from multiprocessing import Pool


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        result = {}
        for line in f:
            m = re.match("(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.", line)
            assert m is not None
            name, speed, fly_time, rest_time = m.groups()
            speed = int(speed)
            fly_time = int(fly_time)
            rest_time = int(rest_time)
                
            result[name] = (speed, fly_time, rest_time)
        return result


def part_1(data):

    reindeers = data.keys()

    rstate = {}
    for r in reindeers:
        speed, fly_time, rest_time = data[r]
        is_flying, count, distance = True, fly_time, 0
        rstate[r] = (is_flying, count, distance)

    for t in range(2503):
            
        for r in reindeers:
            speed, fly_time, rest_time = data[r]
            is_flying, count, distance = rstate[r]

            count -= 1

            if is_flying:
                distance += speed

            if count == 0:
                is_flying = not is_flying
                if is_flying:
                    count = fly_time
                else:
                    count = rest_time

            rstate[r] = (is_flying, count, distance)

    return max(x[2] for x in rstate.values())


def part_2(data):

    reindeers = data.keys()

    rstate = {}
    for r in reindeers:
        speed, fly_time, rest_time = data[r]
        is_flying, count, distance, score = True, fly_time, 0, 0
        rstate[r] = (is_flying, count, distance, score)

    for t in range(2503):
            
        for r in reindeers:
            speed, fly_time, rest_time = data[r]
            is_flying, count, distance, score = rstate[r]

            count -= 1

            if is_flying:
                distance += speed

            if count == 0:
                is_flying = not is_flying
                if is_flying:
                    count = fly_time
                else:
                    count = rest_time

            rstate[r] = (is_flying, count, distance, score)

        winning_d = max(x[2] for x in rstate.values())

        for r in reindeers:
            is_flying, count, distance, score = rstate[r]
            if distance == winning_d:
                score += 1
            rstate[r] = (is_flying, count, distance, score)
        
    return max(x[3] for x in rstate.values())
       

def main():
    data = load()
    p1 = part_1(data)
    p2 = part_2(data)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
