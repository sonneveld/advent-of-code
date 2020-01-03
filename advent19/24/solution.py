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

from collections import Counter
from collections import defaultdict
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import product
from multiprocessing import Pool


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    result = []
    with open(filename) as f:
        data = f.readlines()
        data = [x.rstrip() for x in data]

        return data

# -------------------------------------------------------------------------------------------------------------------
# PART ONE
# -------------------------------------------------------------------------------------------------------------------

def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )

def part_1(data):
    bugs = set()
    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            if ch == "#":
                bugs.add( (x,y) )

    bugs = frozenset(bugs)

    all_spaces = set()
    
    for y in range(5):
        for x in range(5):
            all_spaces.add( (x,y) )

    layout_history = set()

    while True:

        layout_history.add(bugs)

        new_state = set()

        for pos in bugs:
            adj_bugs = get_adj_pos(pos) & bugs
            num_adj_bugs = len(adj_bugs)

            if num_adj_bugs == 1:
                new_state.add(pos)

        for pos in all_spaces:
            if pos in bugs:
                continue
            adj_bugs = get_adj_pos(pos) & bugs

            num_adj_bugs = len(adj_bugs)

            if num_adj_bugs in (1, 2):
                new_state.add(pos)


        new_state = frozenset(new_state)


        rating = 0
        i = 1
        for y in range(5):
            for x in range(5):
                if (x,y) in new_state:
                    rating += i

                i *= 2

        if new_state in layout_history:
            return rating

        bugs = new_state


# -------------------------------------------------------------------------------------------------------------------
# PART TWO
# -------------------------------------------------------------------------------------------------------------------

def print_bugs(bugs_by_depth):
        for depth in bugs_by_depth.keys():
            print()
            print(f'Depth {depth}:')
            bugs = bugs_by_depth[depth]
            for i, b in enumerate(bugs):
                if i % 5 == 0:
                    print()
                if b:
                    print("#", end='')
                else:
                    print(".", end='')
            print()



def left_bugs(bugs):
    x = 0
    for y in range(5):
        yield bugs[y*5 +x]

def right_bugs(bugs):
    x = 4
    for y in range(5):
        yield bugs[y*5 +x]

def top_bugs(bugs):
    y = 0
    for x in range(5):
        yield bugs[y*5 +x]

def bottom_bugs(bugs):
    y = 4
    for x in range(5):
        yield bugs[y*5 +x]

def part_2(data):
    bugs = [False] * 25
    bugs_by_depth = {}
    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            if ch == "#":
                bugs[y*5 + x] = True

    bugs_by_depth[0] = bugs


    def get_at_depth(bugs_by_depth, depth):
        if depth in bugs_by_depth:
            return bugs_by_depth[depth]
        return [False] * 25

    print_bugs(bugs_by_depth)

    for t_minutes in range(200):

        print()
        print()
        print(f"minutes: {t_minutes+1}")

        next_bugs_by_depth = {}


        depth_min = min(bugs_by_depth.keys())
        depth_max = max(bugs_by_depth.keys())

        for depth in range(depth_min-2, depth_max+2):

            bugs = get_at_depth(bugs_by_depth,depth)

            next_bugs = [False]*25

            for i, b in enumerate(bugs):
                y,x = divmod(i, 5)

                # skipp middle
                if (x,y) == (2,2):
                    continue

                adj_pos_list = get_adj_pos( (x,y) )

                adj_bug_count = 0

                for ax, ay in adj_pos_list:

                    if (ax, ay)== (2,2):
                        inner_bugs = get_at_depth(bugs_by_depth,depth+1)

                        if (x,y) == (2-1,2):
                            adj_bug_count += list(left_bugs(inner_bugs)).count(True)

                        if (x,y) == (2+1,2):
                            adj_bug_count += list(right_bugs(inner_bugs)).count(True)

                        if (x,y) == (2,2-1):
                            adj_bug_count += list(top_bugs(inner_bugs)).count(True)

                        if (x,y) == (2,2+1):
                            adj_bug_count += list(bottom_bugs(inner_bugs)).count(True)
                        continue

                    if ax in (0,1,2,3,4) and ay in (0,1,2,3,4):
                        if bugs[ay*5 + ax]:
                            adj_bug_count += 1
                        continue


                    outer_bugs = get_at_depth(bugs_by_depth,depth-1)

                    if ax < 0:
                        nx, ny = 2-1, 2
                        if outer_bugs[ny*5 +nx]:
                            adj_bug_count += 1


                    elif ax >= 5:
                        nx, ny = 2+1, 2
                        if outer_bugs[ny*5 +nx]:
                            adj_bug_count += 1

                    
                    elif ay < 0:
                        nx, ny = 2, 2-1
                        if outer_bugs[ny*5 +nx]:
                            adj_bug_count += 1

                    elif ay >= 5:
                        nx, ny = 2, 2+1
                        if outer_bugs[ny*5 +nx]:
                            adj_bug_count += 1

                if b:
                    next_bugs[i] = adj_bug_count == 1
                else:
                    next_bugs[i] = adj_bug_count in (1,2)


            if next_bugs.count(True) > 0:
                next_bugs_by_depth[depth] = next_bugs

        bugs_by_depth = next_bugs_by_depth
        print_bugs(bugs_by_depth)


    count = 0
    for depth in bugs_by_depth.keys():
        count += get_at_depth(bugs_by_depth,depth).count(True)

    return count


def main():
    data = load()
    part_1_answer = part_1(data)
    part_2_answer = part_2(data)
    print(part_1_answer)
    print(part_2_answer)


if __name__ == "__main__":
    main()
