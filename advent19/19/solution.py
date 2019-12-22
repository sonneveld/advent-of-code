#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import defaultdict
import time
from itertools import product

from functools import lru_cache

import itertools


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
# SOLUTION
# ----------------------------------------------------------------------------------------------------------------------

class Beam:

    def __init__(self, data):
        self.sim_state = SimState('beam', data)
        ret = simulator(self.sim_state)
        assert ret == "INPUT"

    @lru_cache(None)
    def __call__(self, x, y):
        ss = self.sim_state.fork()
        ss.input.append(x)
        ss.input.append(y)
        ret = simulator(ss)
        assert ret == "OUTPUT"
        assert(len(ss.output) == 1)
        value = ss.output.pop(0)
        return value



print_map = {
    0: '░',
    1: '▓',
    2: '█'
}


def get_result_points(beamf, start_x, start_y):
    for y in range(100):
        for x in range(100):
            yield start_x + x, start_y+y


def part_1(data):

    beamf = Beam(data)

    result_points = set(get_result_points(beamf, 684, 937))

    count = 0
    for y in range(50):
        for x in range(50):
            value =  beamf( x, y )

            if (x,y) in result_points:
                value = 2
            
            print(print_map[value], end = '')
            count += value
        print()
    return count




def find_y_range(beamf, x, y):

    # we might not be exactly at beam, but search downwards until
    # find start, then keep going until end

    y_min = None
    y_max = None

    for y_next in itertools.count(y, 1):

        value = beamf(x, y_next)

        if value == 0:
            if y_min is not None:
                break

        elif value == 1:
            found_beam = True
            if y_min is None:
                y_min = y_next
            y_max = y_next

    assert(y_min is not None)
    assert(y_max is not None)

    return y_min, y_max





def search_square(beamf, start_x, start_y, sqlen):
    return beamf(start_x, start_y) == 1 and \
        beamf(start_x+sqlen-1, start_y) == 1 and \
        beamf(start_x, start_y+sqlen-1) == 1 and \
        beamf(start_x+sqlen-1, start_y+sqlen-1) == 1 



def part_2(data):

    beamf = Beam(data)

    # start with a non-zero since beam has some empty columns early on
    x_init = 10

    y_min = 0

    for x in itertools.count(x_init, 1):

        y_min, y_max = find_y_range(beamf, x, y_min)
        y_end = y_max+1

        y_len = y_end - y_min

        if y_len < 100:
            continue
        
        # print(f'{x},{y_min} to {x},{y_max} len:{y_len}')

        for y_search in itertools.count(y_min, 1):

            if y_search + 100 > y_end:
                break

            if search_square(beamf, x, y_search, 100):
                # print("FOUND", x, y_search)

                return x*10000 + y_search



def main():
    data = load()
    v = part_1(data)
    print(v)
    v = part_2(data)
    print(v)


if __name__ == "__main__":
    main()
