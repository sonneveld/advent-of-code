#!/usr/bin/env python3

import sys
import os
import os.path
# import re
# import itertools
# from collections import Counter
# import math
# from dataclasses import dataclass
from functools import lru_cache

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.readlines()
        data = [x.rstrip() for x in data]
        return data


import string


def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )


def parse_map(data):
    open_areas = set()
    partial_portals = {}

    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            if ch == ".":
                open_areas.add( (x,y) )
            elif ch in string.ascii_uppercase:
                partial_portals[ (x,y) ] = ch

    # hack to find keys
    consolidated_portals = set()

    for pos, ch in partial_portals.items():

        adj = get_adj_pos( pos )

        other = None
        for a in adj:
            if a in partial_portals:
                other = a
                break
        assert other is not None

        key_portions = [
            (pos, ch),
            (other, partial_portals[other])
        ]
        key_portions.sort()
        key = ''.join([ch for pos,ch in key_portions])

        poses = frozenset(sorted((pos, other)))

        consolidated_portals.add(( key, poses) )

    # find gateways

    portal_lookup = {}
    for key, poses in consolidated_portals:
        adj = set()
        for p in poses:
            adj |= get_adj_pos(p)
        adj &= open_areas
        adj = list(adj)
        assert(len(adj) == 1)
        portal_lookup[adj[0]] = key

    return open_areas, portal_lookup



def part_1(data):

    open_areas, portal_lookup = parse_map(data)

    @lru_cache(None)
    def lookup_portal(name, ignore=None):
        for pos, pname in portal_lookup.items():
            if pname == name and pos != ignore:
                return pos
        return None

    @lru_cache(None)
    def lookup_portal_2(name):
        result = set()
        for pos, pname in portal_lookup.items():
            if pname == name:
                result.add(pos)
        return result

    @lru_cache(None)
    def get_next_pos(this_pos):

        adj = get_adj_pos(this_pos)
        adj &= open_areas

        if this_pos in portal_lookup:
            pos_name = portal_lookup[this_pos]
            jump_poses = lookup_portal_2(pos_name)
            adj |= jump_poses

        adj -= set([this_pos])

        return adj


    start_pos = lookup_portal('AA')
    end_pos = lookup_portal('ZZ')

    q = []
    q.append( (start_pos, 0) )

    state = {}

    while q:

        pos, dist = q.pop(0)

        if pos not in state or dist < state[pos]:
            state[pos] = dist

        if dist > state[pos]:
            continue

        next_p_list = get_next_pos(pos)

        for next_p in next_p_list:
            q.append( (next_p, dist+1) )


    if False:
        for y in range(130):
            for x in range(130):
                if (x,y) in state:
                    print("%3d "% state[(x,y)], end='')
                else:
                    print("    ", end='')
            print() 

    print(state[end_pos])



def part_2(data):

    open_areas, portal_lookup = parse_map(data)

    @lru_cache(None)
    def lookup_portal(name, ignore=None):
        for pos, pname in portal_lookup.items():
            if pname == name and pos != ignore:
                return pos
        return None

    @lru_cache(None)
    def lookup_portal_2(name):
        result = []
        for pos, pname in portal_lookup.items():
            if pname == name:
                result.append(pos)
        return result



    open_area_x_min = min(p[0] for p in open_areas)
    open_area_x_max = max(p[0] for p in open_areas)
    open_area_y_min = min(p[1] for p in open_areas)
    open_area_y_max = max(p[1] for p in open_areas)


    @lru_cache(None)
    def is_outer_portal(pos):
        return pos[0] in (open_area_x_min, open_area_x_max) or pos[1] in (open_area_y_min, open_area_y_max)


    @lru_cache(None)
    def get_next_pos(this_pos):

        twod_pos = (this_pos[0],this_pos[1])

        adj = get_adj_pos(this_pos)
        adj &= open_areas

        adj = set (  (  (x,y, this_pos[2]) for x,y in adj) )

        if twod_pos in portal_lookup:
            pos_name = portal_lookup[twod_pos]

            jump_poses = set(lookup_portal_2(pos_name))
            if len(jump_poses) == 2:
                jump_poses.remove(twod_pos)
                for jp in jump_poses:
                    if is_outer_portal(twod_pos):
                        adj.add( (jp[0], jp[1], this_pos[2]-1))
                    else:
                        adj.add( (jp[0], jp[1], this_pos[2]+1))

        adj -= set([this_pos])

        return adj


    start_pos = lookup_portal('AA')
    start_pos = (start_pos[0], start_pos[1], 0)
    end_pos = lookup_portal('ZZ')
    end_pos = (end_pos[0], end_pos[1], 0)


    q = []
    q.append( (start_pos, 0) )

    state = {}

    last_zz = None

    while q:

        if end_pos in state:
            break

        q.sort(lambda x: (x[0][2],x[1])  )
        pos, dist = q.pop(0)

        if pos not in state or dist < state[pos]:
            state[pos] = dist

        if dist > state[pos]:
            continue

        next_p_list = get_next_pos(pos)

        for next_p in next_p_list:
            if next_p[2] < 0:
                continue
            q.append( (next_p, dist+1) )


    if False:
        for y in range(130):
            for x in range(130):
                if (x,y) in state:
                    print("%3d "% state[(x,y)], end='')
                else:
                    print("    ", end='')
            print() 

    print(state[end_pos])


def main():
    data = load()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
