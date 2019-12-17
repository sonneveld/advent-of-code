#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import defaultdict
import time
from itertools import product

'''
 	    0	1	2	3	4	5	6	7	8	9	A	B	C	D	E	F
U+258x	▀	▁	▂	▃	▄	▅	▆	▇	█	▉	▊	▋	▌	▍	▎	▏
U+259x	▐	░	▒	▓	▔	▕	▖	▗	▘	▙	▚	▛	▜	▝	▞	▟
'''

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
            # simstate.ip = None
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


# ----------------------------------------------------------------------------------------------------------------------
# PART 1
# ----------------------------------------------------------------------------------------------------------------------

DIRECTIONS = "^v<>"

def capture_screen(data):

    sim_state = SimState('ASCII', data)

    while True:
        ret = simulator(sim_state)

        if ret == "OUTPUT":
            ch = chr(sim_state.output.pop(0))
            yield ch
        elif ret == "DONE":
            break
        else:
            raise Exception(f'unexpected state: {ret}')

def capture_scaffold_state(data, print_it=False):

    scaffold = set()
    robot_pos = None
    robot_direction = None

    pos_x = 0
    pos_y = 0

    for ch in capture_screen(data):

        if ch == "#":
            scaffold.add ( (pos_x, pos_y) )
            pos_x += 1
        elif ch == ".":
            pos_x += 1
        elif ch in DIRECTIONS:
            scaffold.add ( (pos_x, pos_y) )
            robot_pos = (pos_x, pos_y)
            robot_direction = ch
            pos_x += 1
        elif ch == "\n":
            pos_x = 0
            pos_y += 1
        else:
            raise Exception(f'unexpected char: {ch}')

        if print_it:
            print(ch, end='')

    return scaffold, robot_pos, robot_direction


def update_pos(pos, direction):
    assert direction in DIRECTIONS

    if direction == "^":
        return (pos[0], pos[1]-1)
    elif direction == "v":
        return (pos[0], pos[1]+1)
    elif direction == "<":
        return (pos[0]-1, pos[1])
    elif direction == ">":
        return (pos[0]+1, pos[1])

    raise Exception(f"unexpected direction: {direction}")


def update_direction(direction, turn):

    assert turn in "LR"
    assert direction in DIRECTIONS

    if direction == "^":
        if turn == "L":
            return "<"
        if turn == "R":
            return ">"
    elif direction == "v":
        if turn == "L":
            return ">"
        if turn == "R":
            return "<"
    elif direction == "<":
        if turn == "L":
            return "v"
        if turn == "R":
            return "^"
    elif direction == ">":
        if turn == "L":
            return "^"
        if turn == "R":
            return "v"

    raise Exception("unexpected direction/turn: {direction} / {turn}")



def part_1(data):

    scaffold, pos, direction = capture_scaffold_state(data)

    intersections = set()

    while True:

        next_pos = update_pos(pos, direction)

        left_dir = update_direction(direction, "L")
        left_pos = update_pos(pos, left_dir)
        right_dir = update_direction(direction, "R")
        right_pos = update_pos(pos, right_dir)

        # turn
        if next_pos not in scaffold:

            if left_pos in scaffold:
                direction = left_dir
            elif right_pos in scaffold:
                direction = right_dir
            else:
                # END OF THE LINE!
                break

        else:
            # move
            if left_pos in scaffold and right_pos in scaffold:
                intersections.add( pos )
            pos = next_pos

    ap = sum( x*y for x,y in intersections )

    print(ap)



# ----------------------------------------------------------------------------------------------------------------------
# PART 2
# ----------------------------------------------------------------------------------------------------------------------

def generate_move_list(scaffold, pos, direction):
    instructions = []

    while True:

        next_pos = update_pos(pos, direction)

        left_dir = update_direction(direction, "L")
        left_pos = update_pos(pos, left_dir)
        right_dir = update_direction(direction, "R")
        right_pos = update_pos(pos, right_dir)

        # turn
        if next_pos not in scaffold:

            if left_pos in scaffold:
                direction = left_dir
                instructions.append("L")
            elif right_pos in scaffold:
                direction = right_dir
                instructions.append("R")
            else:
                # END OF THE LINE!
                break

        else:
            # move
            instructions.append("1")
            pos = next_pos

    return "".join(instructions)

# replace all the 1's with numbers
# I worried that maybe we would be splitting numbers so I started with 1's
def consolidate(s):
    result = []
    count = 0
    for ch in s:
        if ch in "LRABC":
            if count:
                result.append(f"{count}")
            count = 0
            result.append(ch)
        elif ch == "1":
            count += 1
    if count:
        result.append(f"{count}")
    result = ",".join(result)
    return result

def compile_move_list(move_list):
    for alen, blen, clen in product(range(1, 50), range(1, 50), range(1, 50)):

        prog = move_list

        restr = '([LR1]{%d})'%alen
        m = re.match(restr, prog)
        if m is None: 
            continue
        a = m.group(1)
        prog = prog.replace(a, "A")

        restr = '[A]*([LR1]{%d})'%blen
        m = re.match(restr, prog)
        if m is None: 
            continue
        b = m.group(1)
        prog = prog.replace(b, "B")

        restr = '[AB]*([LR1]{%d})'%clen
        m = re.match(restr, prog)
        if m is None: 
            continue
        c = m.group(1)
        prog = prog.replace(c, "C")

        if "1" in prog or "L" in prog or "R" in prog:
            continue

        prog = consolidate(prog)
        a = consolidate(a)
        b = consolidate(b)
        c = consolidate(c)

        if len(prog) > 20: continue
        if len(a) > 20: continue
        if len(b) > 20: continue
        if len(c) > 20: continue

        return prog, a, b, c

def run_program(data, prog, a, b, c, video=False):
    sim_state = SimState('ASCII', data)
    sim_state.data[0] = 2  # override for part 2

    for entry in (prog, a, b, c):
        for ch in entry:
            sim_state.input.append(ord(ch))
        sim_state.input.append(ord('\n'))

    if video:
        sim_state.input.append(ord('y'))
    else:
        sim_state.input.append(ord('n'))
    sim_state.input.append(ord('\n'))

    dust_value = None

    while True:
        ret = simulator(sim_state) 

        if ret == 'OUTPUT':
            x = sim_state.output.pop(0)
            if x > 0xff:
                dust_value = x
            else:
                ch = chr(x)
                print(ch, end='')
                sys.stdout.flush()
        elif ret == "INPUT":
            x = sys.stdin.read(1)
            if len(x) > 0:
                sim_state.input.append(ord(x))
        elif ret == "DONE":
            break

    print(dust_value)

def part_2(data):
    scaffold, robot_pos, robot_direction = capture_scaffold_state(data)
    move_list = generate_move_list(scaffold, robot_pos, robot_direction)
    prog, a, b, c = compile_move_list(move_list)
    print(f'''
    Main: {prog}
       A: {a}
       B: {b}
       C: {c}''')
    run_program(data, prog, a, b, c)


def main():
    data = load()
    part_1(data)
    part_2(data)


if __name__ == "__main__":
    main()
