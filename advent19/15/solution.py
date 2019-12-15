#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import defaultdict
from dataclasses import dataclass
import time

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = re.findall(r'\-?\d+', f.read())
        data = [int(x) for x in data]
        return data


class SimState(object):
    def __init__(self, name, data_in, extra_mem = 4096):
        self.name = name
        self.data = list(data_in) + [0] * extra_mem
        self.ip = 0
        self.base = 0
        self.input = []
        self.output = []

    def fork(self):
        c = SimState(self.name, self.data, 0)
        c.ip = self.ip
        c.base = self.base
        c.input = list(self.input)
        c.output = list(self.output)
        return c


def simulator(simstate):
    """
    >>> simulator([1,9,10,3,2,3,11,0,99,30,40,50])[0]
    3500
    >>> simulator([1,0,0,0,99])
    [2, 0, 0, 0, 99]
    >>> simulator([2,3,0,3,99])
    [2, 3, 0, 6, 99]
    >>> simulator([2,4,4,5,99,0])
    [2, 4, 4, 5, 99, 9801]
    >>> simulator([1,1,1,4,99,5,6,0,99])
    [30, 1, 1, 4, 2, 5, 6, 0, 99]
    """

    if DEBUG:
        print(f"[{simstate.name}] before: {simstate.data}")

    # ip = 0
    packed_op = None

    def src_parameter(param_index):
        param_type = (packed_op // 100 // (10**param_index) ) % 10
        param_val = simstate.data[simstate.ip + 1 + param_index]

        if param_type == 0:  # position
            return simstate.data[param_val]
        elif param_type == 1:  # immediate
            return param_val
        elif param_type == 2:  # relative
            return simstate.data[param_val + simstate.base]
        else:
            raise Exception(f"[{simstate.name}] unknown src param type: {param_type}")

    def write_param(param_index, value):
        param_type = (packed_op // 100 // (10**param_index) ) % 10
        param_val = simstate.data[simstate.ip + 1 + param_index]

        if param_type == 0:  # position
            simstate.data[param_val] = value
        elif param_type == 2:  # relative
            simstate.data[param_val + simstate.base] = value
        else:
            raise Exception(f"[{simstate.name}] unknown dest param type: {param_type}")

    while True:

        packed_op = simstate.data[simstate.ip]
        op = packed_op % 100

        if DEBUG:
            print("ip:", simstate.ip, 'op:', op, 'instr:',simstate.data[simstate.ip:simstate.ip+4])

        if op == 99:
            simstate.ip = None
            break
    
        # ADD
        elif op == 1:
            a = src_parameter(0)
            b = src_parameter(1)
            write_param(2, a+b)
            simstate.ip += 4

        # MULT
        elif op == 2:
            a = src_parameter(0)
            b = src_parameter(1)
            write_param(2, a*b)

            simstate.ip += 4
    
        # INPUT
        elif op == 3:
            if len(simstate.input) <= 0:
                return 'INPUT'
                # value = input(f"[{simstate.name}] input: ")
                # value = int(value)
                # simstate.input.append(value)

            value = simstate.input.pop(0)

            write_param(0, value)

            simstate.ip += 2

        # OUTPUT
        elif op == 4:
            a = src_parameter(0)
            # print(a)
            # print("out", a)
            simstate.output.append(a)
            simstate.ip += 2
            # return
            return "OUTPUT"

            # return ip, input_buffer, a

        # jmp if != 0
        elif op == 5:
            a = src_parameter(0)
            b = src_parameter(1)

            if a != 0:
                simstate.ip = b
                assert(simstate.ip is not None)
            else:
                simstate.ip += 3

        # jmp if == 0
        elif op == 6:
            a = src_parameter(0)
            b = src_parameter(1)

            if a == 0:
                simstate.ip = b
                assert(simstate.ip is not None)
            else:
                simstate.ip += 3

        # a < b
        elif op == 7:
            a = src_parameter(0)
            b = src_parameter(1)

            if a < b:
                write_param(2, 1)
            else:
                write_param(2, 0)
            simstate.ip += 4

        # a == b
        elif op == 8:
            a = src_parameter(0)
            b = src_parameter(1)

            if a == b:
                write_param(2, 1)
            else:
                write_param(2, 0)
            simstate.ip += 4

        # adjust base
        elif op == 9:
            a = src_parameter(0)
            simstate.base += a
            simstate.ip += 2

        else:
            raise Exception(f"[{simstate.name}] bad op: {op}")

    if DEBUG:
        print(f"[{simstate.name}] after: {simstate.data}")

        print(f"[{simstate.name}] DONE")

    return "DONE"





'''
 	    0	1	2	3	4	5	6	7	8	9	A	B	C	D	E	F
U+258x	▀	▁	▂	▃	▄	▅	▆	▇	█	▉	▊	▋	▌	▍	▎	▏
U+259x	▐	░	▒	▓	▔	▕	▖	▗	▘	▙	▚	▛	▜	▝	▞	▟
'''

def print_points(points):
    if len(points) <= 0:
        return
    sys.stdout.write("\033c")

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    min_x, max_x = -20, 20
    min_y, max_y = -20, 20

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (x,y) in points:
                print("█", end='')
            else:
                print(" ", end='')
        print()
            
def print_move_count(move_count):
    if len(move_count) <= 0:
        return
    sys.stdout.write("\033c")

    min_x = min(p[0] for p in move_count.keys())
    max_x = max(p[0] for p in move_count.keys())
    min_y = min(p[1] for p in move_count.keys())
    max_y = max(p[1] for p in move_count.keys())

    min_x, max_x = -20, 20
    min_y, max_y = -20, 20

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):

            if (x,y) in move_count:
                print("%3d "%move_count[(x,y)], end='')
            else:
                print("    ", end='')
        print()
            

def adjust_point(point, direction):
    if direction == 1:  # north
        return point[0], point[1]-1
    elif direction == 2: # south
        return point[0], point[1]+1
    elif direction == 3: # WEST / LEFT
        return point[0]-1, point[1]
    elif direction == 4: # east
        return point[0]+1, point[1]

    raise Exception(f"bad direction: {direction}")


def part_1(data):

    init_sim_state = SimState('robot', data)
    ret = simulator(init_sim_state)
    assert(ret == "INPUT")

    init_moves = 0
    init_pos = (0,0)

    move_count = {}

    queue = []
    queue.append( (init_moves, init_pos, init_sim_state) )

    open_areas = set()
    open_areas.add(init_pos)

    water_pos = None

    while len(queue) > 0:

        print_move_count(move_count)

        moves, pos, pos_sim_state = queue.pop(0)

        if pos in move_count and move_count[pos] < moves:
            continue

        move_count[pos] = moves
        open_areas.add(pos)

        print()
        print(f'from {pos}')
    
        for direction in (1,2,3,4):

            new_pos = adjust_point(pos, direction)

            sim_state = pos_sim_state.fork()
            sim_state.input.append(direction)
            ret = simulator(sim_state)
            assert ret == "OUTPUT"
            out = sim_state.output.pop(0)

            if out == 2:
                water_pos = new_pos
                print(f"  -> {new_pos} == WATER!!!")

            if out == 1 or out == 2:
                print(f"  -> {new_pos}")
                print(new_pos, 'move')
                queue.append( (moves+1, new_pos, sim_state) )
            else:
                print(f"  -> {new_pos} == WALL")
                pass
   
    print(f'{water_pos} == WATER!!! moves: {move_count[water_pos]}')

    return move_count[water_pos], water_pos, open_areas


def part_2(water_pos, open_areas):

    oxy_set = set()
    oxy_set.add(water_pos)

    t = 0

    while len(oxy_set) < len(open_areas):

        print_points(oxy_set)

        for pos in set(oxy_set):

            for direction in (1,2,3,4):
                new_pos = adjust_point(pos, direction)

                if new_pos not in open_areas:
                    continue
                oxy_set.add(new_pos)

        t += 1

    print_points(oxy_set)
    return t


def main():
    data = load()

    pt1_value, water_pos, open_areas = part_1(data)
    pt2_value = part_2(water_pos, open_areas)

    print()
    print(pt1_value)
    print(pt2_value)


if __name__ == "__main__":
    main()
