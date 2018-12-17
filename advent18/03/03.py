#!/usr/bin/env python3

import re
import collections
import sys

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"


def claim_generator():
    with open(input_filename) as f:
        for line in f:
            line = line.strip()
            m = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
            claim_id, x, y, w, h = [int(x) for x in m.group(1,2,3,4,5)]
            yield (claim_id, x, y, w, h)


# Part 1

claim_count = collections.Counter()

for claim_id, x, y, w, h in claim_generator():
    for i in range(w):
        for j in range(h):
            claim_count[(x+i, y+j)] += 1


claims = [x for x in claim_count.most_common() if x[1] > 1]
print (len(claims))


# Part 2

for claim_id, x, y, w, h  in claim_generator():

    conflict = False
    for i in range(w):
        for j in range(h):
            if claim_count[(x+i, y+j)] != 1:
                conflict = True

    if not conflict:
        print (claim_id)
        break
