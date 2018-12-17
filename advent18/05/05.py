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
    data = f.read().strip()


def react(data):
    data = list(data)

    repeat = True
    while repeat:

        repeat = False

        for i,x in enumerate(data):
            prev = None
            if i > 0:
                prev = data[i-1]

            if prev == None:
                continue
            if prev.lower() != x.lower():
                continue

            if prev.isupper() == x.isupper():
                continue

            data[i] = None
            data[i-1] = None
            repeat = True

        data = [x for x in data if x is not None]

    return data


# Part 1

print (len(react(data)))


# Part 2

result = []
for letter in "abcdefghijklmnopqrstuvwxyz":
    s = react([x for x in data if x.lower() != letter])
    result.append(s)

result.sort(key=len)
print(len(result[0]))
