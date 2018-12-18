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
    data = [x.rstrip() for x in f.readlines()]

OPEN = '.'
TREE = '|'
LUMBERYARD = '#'

state = {}
for y,  row in enumerate(data):
    for x, ch in enumerate(row):
        if ch not in TREE+LUMBERYARD:
            continue
        state[(x,y)] = ch

# input is 50x50, sample is 10x10
SIZE = len(data)



def dump(t, state):

    result = []
    for y in range(SIZE):
        for x in range(SIZE):
            pos = (x,y)
            ch = state.get(pos, OPEN)
            result.append(ch)
        result.append("\n")

    print (f"t = {t}")
    return "".join(result)

def hashstate(state):
    result = []
    for y in range(SIZE):
        for x in range(SIZE):
            pos = (x,y)
            ch = state.get(pos, OPEN)
            result.append(ch)
    return hash("".join(result))

def adjacent_pos(pos):
    return [
        (pos[0]-1, pos[1]),
        (pos[0]+1, pos[1]),
        (pos[0], pos[1]-1),
        (pos[0], pos[1]+1),

        (pos[0]-1, pos[1]-1),
        (pos[0]-1, pos[1]+1),
        (pos[0]+1, pos[1]-1),
        (pos[0]+1, pos[1]+1)

        ]

def get_adjacent(state, pos):
    for p in adjacent_pos(pos):
        yield state.get(p, OPEN)



seen = set()
h = hashstate(state)
seen.add(h)

num_trees = len([x for x in state.values() if x == TREE])
num_lumberyards = len([x for x in state.values() if x == LUMBERYARD])

full_result_table = [num_trees*num_lumberyards]

part1 = None

if DEBUG:
    print(dump(0, state))

for t in range(1, 1000000000+1):
    new_state = {}

    for y in range(SIZE):
        for x in range(SIZE):
            pos = (x,y)

            ch = state.get( pos, OPEN)

            adj = list(get_adjacent(state, pos))
            num_trees = len([x for x in adj if x == TREE])
            num_lumberyards = len([x for x in adj if x == LUMBERYARD])

            if ch == OPEN:
                if num_trees >= 3:
                    ch = TREE

            elif ch == TREE:
                if num_lumberyards >= 3:
                    ch = LUMBERYARD

            elif ch == LUMBERYARD:
                if num_lumberyards < 1 or num_trees < 1:
                    ch = OPEN

            if ch != OPEN:
                new_state[pos] = ch

    state = new_state

    if DEBUG:
        print(dump(t, state))

    num_trees = len([x for x in state.values() if x == TREE])
    num_lumberyards = len([x for x in state.values() if x == LUMBERYARD])

    if t == 10:
        # Part 1
        print(num_trees*num_lumberyards)
    elif t == 1000000000:
        # Part 2
        print(num_trees*num_lumberyards)

    full_result_table.append(num_trees*num_lumberyards)

    h = hashstate(state)
    if h in seen:
        break
    seen.add(h)


# Part 2

full_result_table.reverse()
repeat_start = full_result_table.index(full_result_table[0], 1)
lookup_table = full_result_table[1:repeat_start+1]
lookup_table.reverse()
start_t = len(full_result_table) - len(lookup_table) - 1

index = 1000000000
index -= start_t
remaining = index % len(lookup_table)

print (lookup_table[remaining])
