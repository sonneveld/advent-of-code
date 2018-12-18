#!/usr/bin/env python3

import collections
import itertools
import sys
import os

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"


def dump(recipes, c1, c2):
    display = []
    for i, r in enumerate(recipes):
        if i == c1:
            display.append("("+str(r)+")")
        elif i == c2:
            display.append("["+str(r)+"]")
        else:
            display.append(' '+str(r)+' ')
    print (' '.join(display))


def recipe_generator():
    recipes = [3,7]
    c1 = 0
    c2 = 1

    yield recipes[0]
    yield recipes[1]

    if DEBUG:
        dump(recipes, c1, c2)

    while True:
        s = recipes[c1] + recipes[c2]
        digits = [int(x) for x in str(s)]
        yield from digits
        recipes.extend(digits)
        c1 = (c1+recipes[c1]+1) % len(recipes)
        c2 = (c2+recipes[c2]+1) % len(recipes)

        if DEBUG:
            dump(recipes, c1, c2)


# Part 1

with open(input_filename) as f:
    input = int(f.read().strip())

part1 = itertools.islice(recipe_generator(), input, input+10)
part1 = [str(x) for x in part1]
part1 = "".join(part1)
print (part1)


# Part 2

with open(input_filename) as f:
    input = [int(x) for x in f.read().strip()]

last = collections.deque([], len(input))
count = 0
for r in recipe_generator():
    last.append(r)
    count += 1
    if list(last) == input:
        break

print(count - len(input))
