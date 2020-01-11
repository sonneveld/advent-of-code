#!/usr/bin/env python3

import sys
import os
import os.path
import re

import collections
import functools
import heapq
import itertools
import math
import multiprocessing
import random
import string
import time
import json
import hashlib

from collections import Counter
from collections import defaultdict
from collections import namedtuple
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import permutations
from itertools import product
from multiprocessing import Pool
from math import sqrt

from copy import copy, deepcopy

DEBUG=False

'''
NOTES:

It was way too slow/memory intensive to search all configurations for 
finding the shortest path to move the goal.

However, there is only one empty server, and there is a straight line
path for the goal data to the destination server. So it is a simple 
matter of moving the empty spot to the next position in the goal data
path. Then moving the goal data to it.

Tricky bit was determining some servers that can never be part of a 
part because the data is too big to move anywhere. And also, not to
include the goal data when moving the empty space, because that would
just move the goal data back to where it was :)
'''

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            m = re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s*(\d+)T\s*(\d+)T\s*(\d+)T\s*(\d+)\%', l)
            if m is None:
                continue
            x, y, size, used, avail, percent = (int(x) for x in m.groups())
            data.append([x, y, size, used, avail, percent])

        return data


def part_1(data):

    nodes = {}

    for x, y, size, used, avail, percent in data:
        nodes[x,y] = (size, used, avail)

    pairs = []

    for a, b in product(nodes.keys(), repeat=2):
        if a == b:
            continue
        a_used = nodes[a][1]
        if a_used <= 0:
            continue
        b_avail = nodes[b][2]
        if a_used > b_avail:
            continue

        pairs.append( (a,b) )

    return len(pairs)

def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )


def dump_data(nodes, usage_by_node, size_by_node):

    for y in range(24):
        for x in range(38):
            if (x,y) not in nodes or size_by_node[(x,y)] < 64:
                print("       ", end=" ")
            else:
                print(f'{usage_by_node[(x,y)]:3d}/{size_by_node[(x,y)]:3d}', end=' ')
        print()

def shortest_path(nodes, usage_by_node, size_by_node, src, dest):

    init_steps = 0
    init_pos = src

    q = []
    seen = set()

    q.append ((init_steps, init_pos))

    while q:

        steps, pos = q.pop(0)

        if pos in seen:
            continue

        seen.add(pos)

        next_steps = steps + 1
        for next_pos in get_adj_pos(pos):
            if next_pos not in nodes:
                continue
            if size_by_node[next_pos] > 100:
                continue

            if next_pos == dest:
                return next_steps

            if next_pos in seen:
                continue

            q.append( (next_steps, next_pos) )
            

def part_2(data):

    nodes = set()
    usage_by_node = {}
    size_by_node = {}
    goal_x = 0

    for x, y, size, used, avail, percent in data:
        n = (x,y)
        nodes.add(n)
        usage_by_node[n] = used
        size_by_node[n] = size
        if y == 0:
            goal_x = max(x, goal_x)


    steps = 0

    # we assume no obstacles for moving goal data
    def goal_path():
        g = (goal_x, 0)
        while True:
            g = (g[0]-1, 0)
            yield g
            if g == (0,0):
                break

    def swap_nodes(a, b):
        av = usage_by_node[a]
        bv = usage_by_node[b]
        usage_by_node[a] = bv
        usage_by_node[b] = av

    goal = (goal_x, 0)
    num_steps = 0

    # print('goal path', list(goal_path()))
    for next_goal in goal_path():

        # clear out path ahead
        empty_node = None
        for n in nodes:
            if usage_by_node[n] <= 0:
                empty_node = n
                break
        assert empty_node is not None

        num_steps += shortest_path(nodes-set([goal]), usage_by_node, size_by_node, empty_node, next_goal)
        swap_nodes(empty_node, next_goal)

        # move the goal data
        num_steps += 1
        swap_nodes(goal, next_goal)
        
        goal = next_goal


    return num_steps


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
