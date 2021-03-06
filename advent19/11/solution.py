#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import defaultdict


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = re.findall(r'\-?\d+', f.read())
        data = [int(x) for x in data]
        # data = f.readline()
        # data = data.split(",")
        # data = [int(x) for x in data]
        return data


class SimState(object):
    def __init__(self, name, data):
        self.name = name
        self.data = list(data) + [0] * 1000
        self.ip = 0
        self.base = 0
        self.input = []
        self.output = []


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
        # guessing at future param types
        # elif param_type == 2:
            # return simstate.ip + param_val
        else:
            raise Exception(f"[{simstate.name}] unknown src param type: {param_type}")

    def write_param(param_index, value):
        param_type = (packed_op // 100 // (10**param_index) ) % 10
        param_val = simstate.data[simstate.ip + 1 + param_index]

        if param_type == 0:  # position
            simstate.data[param_val] = value
        elif param_type == 2:  # relative
            simstate.data[param_val + simstate.base] = value
        # guessing at future param types
        # elif param_type == 2:
            # simstate.data[simstate.ip + param_val] = value
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
                value = input(f"[{simstate.name}] input: ")
                value = int(value)
                simstate.input.append(value)

            value = simstate.input.pop(0)

            # simstate.data[a] = value

            write_param(0, value)

            simstate.ip += 2

        # OUTPUT
        elif op == 4:
            a = src_parameter(0)
            # print(a)
            # print("out", a)
            simstate.output.append(a)
            simstate.ip += 2
            return
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


def part_1(data):

    pos_x = 0
    pos_y = 0
    direction = 0
    colour_state = defaultdict(int)

    sim_state = SimState('robot', data)

    painted = set()

    while True:
        col = colour_state[(pos_x, pos_y)]
        sim_state.input.append(col)
        ret = simulator(sim_state)
        if ret == "DONE": break
        new_col = sim_state.output.pop(0)
        ret = simulator(sim_state)
        if ret == "DONE": break
        new_dir = sim_state.output.pop(0)
        assert(len(sim_state.output) == 0)
        colour_state[(pos_x, pos_y)] = new_col

        painted.add((pos_x, pos_y))
        if new_dir == 0:
            direction -= 1
        elif new_dir == 1:
            direction += 1
        else:
            raise Exception(f"bad direction offset: {new_dir}")
        direction = direction % 4
        if direction == 0:
            pos_y -= 1
        elif direction == 1:
            pos_x += 1
        elif direction == 2:
            pos_y += 1
        elif direction == 3:
            pos_x -= 1
        else:
            raise Exception(f"bad direction: {direction}")

    return len(painted)


    


def part_2(data):

    pos_x = 0
    pos_y = 0
    direction = 0
    colour_state = defaultdict(int)
    colour_state[(pos_x, pos_y)] = 1


    sim_state = SimState('robot', data)

    painted = set()

    while True:
        col = colour_state[(pos_x, pos_y)]
        sim_state.input.append(col)
        ret = simulator(sim_state)
        if ret == "DONE": break
        new_col = sim_state.output.pop(0)
        ret = simulator(sim_state)
        if ret == "DONE": break
        new_dir = sim_state.output.pop(0)
        assert(len(sim_state.output) == 0)
        colour_state[(pos_x, pos_y)] = new_col

        painted.add((pos_x, pos_y))
        if new_dir == 0:
            direction -= 1
        elif new_dir == 1:
            direction += 1
        else:
            raise Exception(f"bad direction offset: {new_dir}")
        direction = direction % 4
        if direction == 0:
            pos_y -= 1
        elif direction == 1:
            pos_x += 1
        elif direction == 2:
            pos_y += 1
        elif direction == 3:
            pos_x -= 1
        else:
            raise Exception(f"bad direction: {direction}")

    pos_x_all = set()
    pos_y_all = set()
    for pos_x, pos_y in colour_state.keys():
        pos_x_all.add(pos_x)
        pos_y_all.add(pos_y)

    x_min, x_max = min(pos_x_all), max(pos_x_all)
    y_min, y_max = min(pos_y_all), max(pos_y_all)
    
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            col = colour_state[(x, y)]
            if col != 0:
                print('X', end = '')
            else:
                print(" ", end = '')
        print()

    

def main():
    data = load()

    value = part_1(data)
    print(value)

    part_2(data)



if __name__ == "__main__":
    main()
