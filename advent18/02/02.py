#!/usr/bin/env python3

import itertools
import collections
import sys

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

data = []
with open(input_filename) as f:
    data = [x.strip() for x in f.readlines()]


# Part 1

boxes_with_2 = 0
boxes_with_3 = 0

for row in data:

    count = collections.Counter(row)

    count2 = len( [x for x in count.most_common() if x[1] == 2])
    count3 = len( [x for x in count.most_common() if x[1] == 3])

    if count2 > 0:
        boxes_with_2 += 1
    if count3 > 0:
        boxes_with_3 += 1


print (boxes_with_2 * boxes_with_3)


# Part 2

for left in data:
    for right in data:

        zipped = list(zip(left, right))

        different = len([x for x in zipped if x[0] != x[1]])
        if different == 1:
            same = "".join([x[0] for x in zipped if x[0] == x[1]])

print (same)
