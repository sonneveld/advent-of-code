#!/usr/bin/env python3

import re
import collections
import sys
import os

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    data = f.read().strip()


# Part 1

sum = 0
for i, x in enumerate(data):
    x = int(x)
    next_index = (i+1)%len(data)
    next = int(data[next_index])
    if x == next:
        sum += x
print(sum)


# Part 2

sum = 0
for i, x in enumerate(data):
    x = int(x)
    next_index = (i+len(data)//2)%len(data)
    next = int(data[next_index])
    if x == next:
        sum += x
print(sum)
