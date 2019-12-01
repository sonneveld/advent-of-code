#!/usr/bin/env python3

import re
import collections
import sys
import os
from heapq import heappush, heappop
from functools import lru_cache
import random

sys.setrecursionlimit(2000)

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

data = []

with open(input_filename) as f:
    for line in f:
        x,y,z,r = [int(x) for x in re.findall(r'[\-\+]?[\d]+', line)]
        data.append( (x,y,z,r) )


def calc_manhattan_distance(x1,y1,z1, x2,y2,z2):
    return abs(x1-x2) + abs(y1-y2) + abs (z1-z2)


def spheres_collide(s1, s2):
    distance = calc_manhattan_distance(s1[0], s1[1], s1[2], s2[0], s2[1], s2[2])
    return  s1[3]+s2[3] >= distance

result = []
for x,y,z,r in data:
    mh = calc_manhattan_distance(0,0,0,x,y,z)
    result.append((mh,x,y,z,r))

result.sort()

for x in result:
    print (x)
