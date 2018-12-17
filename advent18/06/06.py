#!/usr/bin/env python3

import collections
import itertools
import re
import sys

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

data = []
with open(input_filename) as f:
    data = [x.strip() for x in f.readlines()]
    data = [x.split(',') for x in data]
    data = [ (int(x[0]), int(x[1])) for x in data ]


def get_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Part 1

avail = set(data)
ranges = {}

for x in range(-100, 500):
    for y in range(-100, 500):

        pos = (x,y)
        if pos in data:
            result = [pos]
        else:
            manhattans = [(get_manhattan(pos, entry), entry) for entry in data]
            manhattans.sort()
            closest_score = manhattans[0][0]
            manhattans = [x[1] for x in manhattans if x[0] == closest_score]
            result = manhattans

        if pos[0] in [-100, 499] or pos[1] in [-100, 499]:
            for entry in result:
                if entry in avail:
                    avail.remove(entry)

        ranges[pos] = result

result = []

for entry in avail:
    size = len([x for x in ranges.values() if len(x) == 1 and entry in x])
    result.append(  (size, entry) )

result.sort(reverse = True)
print(result[0][0])


# Part 2

ranges = {}

for x in range(-100, 500):
    for y in range(-100, 500):
        pos = (x,y)
        total_manhattans = sum([get_manhattan(pos, entry) for entry in data])
        ranges[pos] = total_manhattans < 10000

print (len([x for x in ranges.values() if x]))
