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
        result = []
        for line in f:
            m = re.match("(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+)\.", line)
            assert m is not None
            person, lg, value, other = m.groups()
            value = int(value)
            if lg == "lose":
                value = -value
                
            result.append(  (person, other, value) )
        return result


def part_1(data):

    def lookup_person_other(p, o):
        for x in data:
            if x[0] == p and x[1] == o:
                return x[2]
        raise Exception()

    scores = set()
    people = set( x[0] for x in data )

    for setting in permutations(people):

        score = 0

        for i,p in enumerate(setting):

            left = setting[(i-1) % len(setting)]
            right = setting[(i+1) % len(setting)]

            score += lookup_person_other(p, left)
            score += lookup_person_other(p, right)

        if DEBUG:
            print (score, setting)
            
        scores.add(score)

    return max(scores)

def part_2(data):

    def lookup_person_other(p, o):
        if p == "You" or o == "You":
            return 0
        for x in data:
            if x[0] == p and x[1] == o:
                return x[2]
        raise Exception()

    scores = set()
    people = set( x[0] for x in data )
    people.add("You")

    for setting in permutations(people):

        score = 0

        for i,p in enumerate(setting):

            left = setting[(i-1) % len(setting)]
            right = setting[(i+1) % len(setting)]

            score += lookup_person_other(p, left)
            score += lookup_person_other(p, right)

        if DEBUG:
            print (score, setting)

        scores.add(score)

    return max(scores)
       

def main():
    data = load()
    p1 = part_1(data)
    p2 = part_2(data)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
