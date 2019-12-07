#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools

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
        self.data = list(data)
        self.ip = 0
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
        val = simstate.data[simstate.ip + 1 + param_index]

        if param_type == 0:
            return simstate.data[val]
        elif param_type == 1:
            return val
        # guessing at future param types
        # elif param_type == 2:
            # return simstate.ip + val
        else:
            raise Exception(f"[{simstate.name}] unknown param type: {param_type}")

    def dest_parameter(param_index):
        if DEBUG:
            param_type = (packed_op // 100 // (10**param_index) ) % 10
            # assert(param_type == 0)
            if param_type != 0:
                print(f"[{simstate.name}] ip:{simstate.ip} WARNING dest parameter is not position")
        val = simstate.data[simstate.ip + 1 + param_index]
        return val

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
            c = dest_parameter(2)
            simstate.data[c] = a + b
            simstate.ip += 4

        # MULT
        elif op == 2:
            a = src_parameter(0)
            b = src_parameter(1)
            c = dest_parameter(2)
            simstate.data[c] = a * b
            simstate.ip += 4
    
        # INPUT
        elif op == 3:
            a = dest_parameter(0)

            if len(simstate.input) <= 0:
                value = input(f"[{simstate.name}] input: ")
                value = int(value)
                simstate.input.append(value)

            value = simstate.input.pop(0)

            simstate.data[a] = value
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
            c = dest_parameter(2)

            if a < b:
                simstate.data[c] = 1
            else:
                simstate.data[c] = 0
            simstate.ip += 4

        # a == b
        elif op == 8:
            a = src_parameter(0)
            b = src_parameter(1)
            c = dest_parameter(2)

            if a == b:
                simstate.data[c] = 1
            else:
                simstate.data[c] = 0
            simstate.ip += 4

        else:
            raise Exception(f"[{simstate.name}] bad op: {op}")

    if DEBUG:
        print(f"[{simstate.name}] after: {simstate.data}")

    # print (f"[{simstate.name}] DONE")
    return



def part_1(data):

    solutions = []

    for phases in itertools.permutations([0, 1, 2, 3, 4], 5):
        # print('--', phases)

        a_phase, b_phase, c_phase, d_phase, e_phase = phases

        a_state = SimState('a', data)
        b_state = SimState('b', data)
        c_state = SimState('c', data)
        d_state = SimState('d', data)
        e_state = SimState('e', data)

        a_state.input.append(a_phase)
        b_state.input.append(b_phase)
        c_state.input.append(c_phase)
        d_state.input.append(d_phase)
        e_state.input.append(e_phase)

        e_out = 0

        a_state.input.append(e_out)
        simulator(a_state)
        if a_state.ip is None: break
        a_out = a_state.output.pop(0)
        # print("a_out", a_out)

        b_state.input.append(a_out)
        simulator(b_state)
        if b_state.ip is None: break
        b_out = b_state.output.pop(0)
        # print("b_out", b_out)

        c_state.input.append(b_out)
        simulator(c_state)
        if c_state.ip is None: break
        c_out = c_state.output.pop(0)
        # print("c_out", c_out)

        d_state.input.append(c_out)
        simulator(d_state)
        if d_state.ip is None: break
        d_out = d_state.output.pop(0)
        # print("d_out", d_out)

        e_state.input.append(d_out)
        simulator(e_state)
        if e_state.ip is None: break
        e_out = e_state.output.pop(0)
        # print("e_out", e_out)

        solutions.append([e_out, phases])


    solutions.sort()
    return solutions[-1][0]


def part_2(data):

    solutions = []

    for phases in itertools.permutations([5,6,7,8,9], 5):
        # print('--', phases)

        a_phase, b_phase, c_phase, d_phase, e_phase = phases

        a_state = SimState('a', data)
        b_state = SimState('b', data)
        c_state = SimState('c', data)
        d_state = SimState('d', data)
        e_state = SimState('e', data)

        a_state.input.append(a_phase)
        b_state.input.append(b_phase)
        c_state.input.append(c_phase)
        d_state.input.append(d_phase)
        e_state.input.append(e_phase)

        e_out = 0

        while True:
            a_state.input.append(e_out)
            simulator(a_state)
            if a_state.ip is None: break
            a_out = a_state.output.pop(0)
            # print("a_out", a_out)

            b_state.input.append(a_out)
            simulator(b_state)
            if b_state.ip is None: break
            b_out = b_state.output.pop(0)
            # print("b_out", b_out)

            c_state.input.append(b_out)
            simulator(c_state)
            if c_state.ip is None: break
            c_out = c_state.output.pop(0)
            # print("c_out", c_out)

            d_state.input.append(c_out)
            simulator(d_state)
            if d_state.ip is None: break
            d_out = d_state.output.pop(0)
            # print("d_out", d_out)

            e_state.input.append(d_out)
            simulator(e_state)
            if e_state.ip is None: break
            e_out = e_state.output.pop(0)
            # print("e_out", e_out)

        solutions.append([e_out, phases])


    solutions.sort()
    return solutions[-1][0]


def main():
    data = load()

    value = part_1(data)
    print(value)

    value = part_2(data)
    print(value)



if __name__ == "__main__":
    main()
