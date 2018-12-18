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
    data = [ [int(y) for y in x.strip().split()] for x in f.readlines()]

# Part 1

checksum = 0
for row in data:
    checksum += max(row) - min(row)

print (checksum)


# Part 2

def find_divisible(nums):
    for x in nums:
        for y in nums:
            if x != y and x % y == 0:
                return (x,y)
    return None,None

result = 0
for row in data:
    x,y = find_divisible(row)
    result += x // y
print(result)
