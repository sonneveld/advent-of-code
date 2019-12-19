#!/usr/bin/env python3

import sys
import os
import os.path
# import re
# import itertools
# from collections import Counter
# import math
# from dataclasses import dataclass

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.readlines()
        data = [x.strip() for x in data]
        return data


def parse_map(data):
    open_areas = set()
    keys = {}
    doors = {}
    robots = []

    for pos_y, line in enumerate(data):
        if False:
            print(line)
        for pos_x, ch in enumerate(line):
            if ch != "#":
                open_areas.add( (pos_x, pos_y) )
            
            if ch == "@":
                robots.append( (pos_x, pos_y) )

            if ch.islower():
                keys[ ch] = (pos_x, pos_y) 

            if ch.isupper():
                doors[ ch] = (pos_x, pos_y) 

    if False:
        print('robots')
        for v in robots:
            print('   ', v)

        print('keys')
        for k,v in sorted( keys.items() ):
            print('   ', k,v)

        print('doors')
        for k,v in sorted( doors.items() ):
            print('   ', k,v)

    return open_areas, robots, keys, doors






def get_adj_pos(pos):
    return set( ( 
        (pos[0]-1, pos[1]), 
        (pos[0]+1, pos[1]), 
        (pos[0], pos[1]-1),  
        (pos[0], pos[1]+1) 
    ) )




# fairly sure this is suboptimal
def shortest_path(open_areas, pos_src, pos_dest):

    state = {}

    q = []
    q.append( (0, pos_src) )

    while len(q) > 0:

        dist,pos = q.pop(0)
        if pos in state and state[pos] <= dist:
            continue

        if pos == pos_dest:
            return dist

        state[pos] = dist

        adj = get_adj_pos(pos)
        adj &= open_areas
        for a in adj:
            new_dist = dist+1
            if a in state and state[a] <= new_dist:
                continue
            q.append( (new_dist, a) )


    if pos_dest not in state:
        return None
    return state[pos_dest]




def flood_fill(open_areas, init_pos, state=None):

    if state is None:
        state = {}

    q = []
    q.append( (0,init_pos) )

    while q:
        q.sort()

        d, p = q.pop(0)

        if p not in open_areas:
            continue

        if p in state and state[p] < d:
            continue

        state[p] = d

        for adj_p in get_adj_pos(p):
            if adj_p not in open_areas:
                continue
            q.append( (d+1, adj_p))

    return state


# use flood fill to walk back
def walk_back(state, key_pos):

    path = []
    path.append(key_pos)

    while True:

        new_pos_list = []

        for p in path:
            distance = state[p]
            adj_pos_list = get_adj_pos(p)
            for adj_pos in adj_pos_list:
                if adj_pos in path:
                    continue
                if adj_pos not in state:
                    continue
                if state[adj_pos] >= distance:
                    continue
                new_pos_list.append(adj_pos)

        if len(new_pos_list) == 0:
            break

        for p in new_pos_list:
            if p not in path:
                path.append(p)

    return path



def precalculate(open_areas, robots, keys, doors):

    state = {}
    for robot in robots:
        state = flood_fill(open_areas, robot, state)

    # print ranges
    if False:
        for y in range(81):
            for x in range(81):

                if (x,y) in state:
                    print("%3d "%state[x,y], end = '')
                else:
                    print("    ", end='')

            print()

    used_spaces = set()

    def door_for_pos(pos):
        for door_name, door_pos in doors.items():
            if door_pos == pos:
                return door_name
        return None

    depends_per_key = {}

    for key_name, key_post in sorted(keys.items()):
        if False:
            print()
            print()
            print()
            print(key_name)
            print()
        path = walk_back(state, keys[key_name])

        dependencies = set()
        for pos in reversed(path):
            door_name = door_for_pos(pos)
            if door_name is not None:
                dependencies.add(door_name.lower())

        if False:
            print(key_name, dependencies)

        depends_per_key[key_name] = dependencies

        used_spaces |= set(path)

        if False:
            for y in range(81):
                for x in range(81):
                    if (x,y) in path:
                        print ("███ ", end='')
                    elif (x,y) in state:
                        print("%3d "%state[x,y], end = '')
                    else:
                        print("    ", end='')
                print()


    # print used spaces
    if False:
        for y in range(81):
            for x in range(81):
                if (x,y) in used_spaces:
                    print ("███ ", end='')
                else:
                    print("    ", end='')
            print()


    distance_cache = {}

    key_names = list(sorted(keys.keys()))
    for first_key_name, first_key_pos in keys.items():
        for second_key_name, second_key_pos in keys.items():

            distance = shortest_path(open_areas, first_key_pos, second_key_pos)

            if distance is not None:
                distance_cache[ (first_key_pos, second_key_pos) ] = distance
                distance_cache[ (second_key_pos, first_key_pos) ] = distance



    robot_keys = {}


    for first_key_name, first_key_pos in keys.items():
        for robot_index, robot in enumerate(robots):
            distance = shortest_path(open_areas, robot, first_key_pos)
            if distance is not None:
                distance_cache[ (robot, first_key_pos) ] = distance
                distance_cache[ (first_key_pos, robot) ] = distance

                robot_keys[first_key_name] = robot_index


    
    return robots, depends_per_key, distance_cache, keys, robot_keys






class WalkState:
    __slots__ = ['robot_poses', 'owned_keys', 'walked']
    
    def __init__(self, robot_poses, owned_keys, walked):
        self.robot_poses = tuple(robot_poses)
        self.owned_keys = frozenset(owned_keys)
        self.walked = walked

    def __lt__(self, other):
        return self.walked < other.walked

    def process(self, depends_per_key, distance_cache, key_info, robot_keys):

        available_keys = set()
        for key_name, depends in depends_per_key.items():
            if len(depends - self.owned_keys) == 0:
                available_keys.add(key_name)

        for key_name in available_keys:
            if key_name in self.owned_keys:
                continue
            key_pos = key_info[key_name]

            robot_i = robot_keys[key_name]
            robot_pos = self.robot_poses[robot_i]

            dist = distance_cache[ robot_pos, key_pos]

            new_robot_poses = list(self.robot_poses)
            new_robot_poses[robot_i] = key_pos

            yield WalkState(new_robot_poses, self.owned_keys|set(key_name), self.walked+dist)


def find_minimal_steps(data_open_areas, data_robots, data_keys, data_doors):

    init_robot_poses, depends_per_key, distance_cache, key_info, robot_keys = \
        precalculate(data_open_areas, data_robots, data_keys, data_doors)

    init_ws = WalkState(init_robot_poses, set(), 0)

    ranks = [None]*32
    for x in range(32):
        ranks[x] = {}

    rank_i = len(init_ws.owned_keys)
    next_rank = ranks[rank_i]
    next_rank[ (init_ws.owned_keys, init_ws.robot_poses)] = init_ws

    for x in range(27):
        print('rank', x, len(ranks[x]))
        cur_rank = ranks[x]
        
        for ws in cur_rank.values():
            for next_ws in ws.process(depends_per_key, distance_cache, key_info, robot_keys):
                rank_i = len(next_ws.owned_keys)
                next_rank = ranks[rank_i]
                k = (next_ws.owned_keys, next_ws.robot_poses)
                if k not in next_rank or next_ws.walked < next_rank[k].walked:
                    next_rank[k] = next_ws

    cur_rank = ranks[len(data_keys)]
    best_ws = min([(ws.walked, ws) for ws in cur_rank.values()])
    best_ws = best_ws[1]
    print (best_ws.walked, ''.join(sorted(best_ws.owned_keys)))


def part_1(data):

    data_open_areas, data_robots, data_keys, data_doors = parse_map(data)

    find_minimal_steps(data_open_areas, data_robots, data_keys, data_doors)



def part_2(data):

    data_open_areas, data_robots, data_keys, data_doors = parse_map(data)

    assert(len(data_robots)==1)
    robot = data_robots[0]

    # make adjustments to map
    data_open_areas -= get_adj_pos(robot)
    data_open_areas.remove(robot)
    data_robots = (
        (robot[0]-1, robot[1]-1),
        (robot[0]-1, robot[1]+1),
        (robot[0]+1, robot[1]-1),
        (robot[0]+1, robot[1]+1),
    )

    find_minimal_steps(data_open_areas, data_robots, data_keys, data_doors)



def main():
    data = load()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
