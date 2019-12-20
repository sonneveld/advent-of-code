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
    def __init__(self, name, data_in):
        self.name = name
        self.data = list(data_in) + [0] * 1000
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
            # if param_val == 0:
            #     return 2
            return simstate.data[param_val]
        elif param_type == 1:  # immediate
            return param_val
        elif param_type == 2:  # relative
            # if param_val + simstate.base == 0:
            #     return 2
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
                return 'INPUT'
                # value = input(f"[{simstate.name}] input: ")
                # value = int(value)
                # simstate.input.append(value)

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


def part_1(data):

    screen = defaultdict(int)

    sim_state = SimState('game', data)
    while True:
        ret = simulator(sim_state)
        if ret != "OUTPUT": break
        x = sim_state.output.pop(0)

        ret = simulator(sim_state)
        if ret != "OUTPUT": break
        y = sim_state.output.pop(0)
        
        ret = simulator(sim_state)
        if ret != "OUTPUT": break
        tile = sim_state.output.pop(0)

        screen[(x,y)] = tile

    block_count = 0
    for k,v in screen.items():
        if v == 2:
            block_count += 1

    return block_count




char_map = {
    0: ' ',
    1: '|',
    2: 'X',
    3: '^',
    4: 'o',
}

def print_screen(screen_orig, quarters, score, paddle, ball):

    screen = defaultdict(int, screen_orig)

    if paddle:
        screen[paddle] = 3
    if ball:
        screen[ball] = 4

    x_set = set([0, 39])
    y_set = set([0, 23])

    block_count = 0
    for k,v in screen.items():
        x_set.add(k[0])
        y_set.add(k[1])

    x_begin, x_end = min(x_set), max(x_set)+1
    y_begin, y_end = min(y_set), max(y_set)+1

    print(f'score: {score}     ---   quarters: {quarters}')
    for y in range(min(y_set), max(y_set)+1):
        for x in range(min(x_set), max(x_set)+1):
            print(char_map[screen[(x,y)]], end='')
        print()

def part_2(data):

    score = None
    screen = defaultdict(int)

    sim_state = SimState('game', data)
    sim_state.data[0] = 2
    quarters = "?"

    paddle = None
    ball = None

    def process_input():
        if paddle and paddle[0] < ball[0]:
            sim_state.input.append(1)
        elif paddle and paddle[0] > ball[0]:
            sim_state.input.append(-1)
        else:
            sim_state.input.append(0)

    while True:
        if False:
            print_screen(screen, quarters, score, paddle, ball)

        ret = simulator(sim_state)
        if ret == "OUTPUT":
            if (len(sim_state.output) >= 3):
                x = sim_state.output.pop(0)
                y = sim_state.output.pop(0)
                tile = sim_state.output.pop(0)
                assert(len(sim_state.output) == 0)

                if x == -1 and y == 0 and tile not in [0,1,2,3, 4]:
                    score = tile
                elif tile in [0,1,2]:
                    screen[(x,y)] = tile
                elif tile == 3:
                    paddle = (x,y)
                elif tile == 4:
                    ball = (x,y)

        elif ret == "INPUT":
            process_input()
        else: 
            break

    if False:
        print_screen(screen, quarters, score, paddle, ball)

    return score
    

def main():
    data = load()

    value = part_1(data)
    print(value)

    value = part_2(data)
    print(value)



if __name__ == "__main__":
    main()
