#!/usr/bin/env python3

import re
import collections
import sys
import multiprocessing

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    serial_number = int(f.read())


values = {}
for x in range(1, 300+1):
    for y in range(1, 300+1):
        rack_id = x + 10
        power_level = rack_id * y
        power_level += serial_number
        power_level *= rack_id
        power_level = int(str(power_level)[-3])
        power_level -= 5
        values[(x,y)] = power_level


# Part 1

max = None
max_x = None
max_y = None
for x in range(1, 300-3):
    for y in range(1, 300-3):
        total = 0
        for xx in range(3):
            for yy in range(3):
                total += values[x+xx, y+yy]
        if max is None or total > max:
            max = total
            max_x = x
            max_y = y

print (f"{max_x},{max_y}")


# Part 2

# this is terrible. Check out Summed-Area Tables
# https://en.wikipedia.org/wiki/Summed-area_table

def get_value(coord):
    x,y = coord

    max = None
    max_x = None
    max_y = None
    max_s = None

    total = 0

    for s in range(1, 300+1):
        if x+s > 300:
            continue
        if y+s > 300:
            continue

        poses = set()
        for xx in range(s):
            poses.add( (x+xx, y+s-1)   )
        for yy in range(s):
            poses.add(  (x+s-1, y+yy)  )

        total += sum([values[x] for x in poses])

        if max is None or total > max:
            max = total
            max_x = x
            max_y = y
            max_s = s

    if max is not None:
        return (max, max_x, max_y, max_s)
    return None


pool = multiprocessing.Pool(processes=8)

coords = []
for x in range(1, 300+1):
    for y in range(1, 300+1):
            coords.append( (x,y) )

results = pool.map(get_value, coords)
results = [x for x in results if x is not None]
results.sort(key = lambda x: x[0], reverse=True)
_, x, y, s = results[0]

print (f"{x},{y},{s}")
