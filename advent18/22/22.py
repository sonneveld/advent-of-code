#!/usr/bin/env python3

import re
import collections
import sys
import os
from heapq import heappush, heappop
from functools import lru_cache

sys.setrecursionlimit(2000)

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    data = f.read()

LRU_CACHE_SIZE = 131072

depth, target_x, target_y = [int(x) for x in re.findall(r'[\-\+]?[\d]+', data)]
target = (target_x, target_y)
mouth = (0,0)

@lru_cache(maxsize=LRU_CACHE_SIZE)
def calc_erosion_level(x, y):
    return (calc_geological_index(x,y) + depth) % 20183

@lru_cache(maxsize=LRU_CACHE_SIZE)
def calc_geological_index(x, y):
    pos = (x,y)
    if pos == mouth:
        return 0
    if pos == target:
        return 0
    if y == 0:
        return 16807*x
    if x == 0:
        return 48271 * y

    return calc_erosion_level(x-1, y) * calc_erosion_level(x, y-1)

def calc_type(x,y):
    return calc_erosion_level(x,y) % 3


# part 1

risk_level = {}
risk_level[ (0,0) ] = calc_type(0,0)

for y in range(0, target[1]+1):
    for x in range(0, target[0]+1):
        if (x,y) == (0,0):
            continue
        risk_level[(x,y)] = calc_type(x,y) + risk_level.get( (x,y-1), 0) + risk_level.get( (x-1, y), 0) - risk_level.get( (x-1, y-1), 0)

print(risk_level[target])



# part 2

NEITHER, TORCH, CLIMBING = (0, 1, 2)
tool_display_lookup = 'ntc'

type_name_lookup = ('rocky', 'wet', 'narrow')
type_display_lookup = '.=|'

tool_lookup = ( (CLIMBING, TORCH), (CLIMBING, NEITHER), (TORCH, NEITHER), )

def calc_adjacent(x,y):
    return (
        (x, y+1),
        (x+1, y),
        (x-1, y),
        (x, y-1),
    )


def dump():
    print('''
. rocky  - (c)limbing gear or (t)orch
= wet    - (c)limbing gear or (n)either
| narrow - (t)orch or (n)either''')

    display_lookup = {}
    for (k,cost) in sorted(cost_table.items()):
        x,y,tool = k
        at_type = type_display_lookup[calc_type(x,y)]
        display_lookup[(x,y)] = display_lookup.get( (x,y), [at_type[:1]]) + [f'{tool_display_lookup[tool]}{cost:04}']

    for y in range(0, target[1]+1):
        for x in range(0, target[0]+1):
            v = ' '.join(display_lookup.get((x,y), []))
            print(f'{v:13} | ', end = '')
        print()


cost_table = {}

queue = []
heappush(queue, (0, 0, 0, TORCH))

while queue:

    cost, x, y, tool = heappop(queue)

    best_cost = cost_table.get( (x,y, tool) , None)
    if best_cost is not None and cost >= best_cost:
        continue

    if DEBUG:
        print(cost, x, y, tool)

    cost_table[(x,y, tool)] = cost

    if (x,y, tool) == (target_x, target_y, TORCH):
        break

    for other_tool in (t for t in tool_lookup[calc_type(x, y)] if t != tool):
        heappush(queue, (cost+7, x, y, other_tool))

    for next_x, next_y in calc_adjacent(x,y):
        if next_x < 0 or next_y < 0:
            continue
        next_type = calc_type(next_x, next_y)
        next_tools = tool_lookup[next_type]
        if tool in next_tools:
            heappush(queue, (cost+1, next_x, next_y, tool))

if DEBUG:
    dump()

print (cost_table[ (target[0], target[1], TORCH)])
