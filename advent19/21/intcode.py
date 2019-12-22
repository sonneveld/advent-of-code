#!/usr/bin/env python3

import sys
import re

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



def _src_param(simstate, packed_op, param_index):
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

def _write_param(simstate, packed_op, param_index, value):
    param_type = (packed_op // 100 // (10**param_index) ) % 10
    param_val = simstate.data[simstate.ip + 1 + param_index]

    if param_type == 0:  # position
        simstate.data[param_val] = value
    elif param_type == 2:  # relative
        simstate.data[param_val + simstate.base] = value
    else:
        raise Exception(f"[{simstate.name}] unknown dest param type: {param_type}")


def simulator(simstate):

    if DEBUG:
        print(f"[{simstate.name}] before: {simstate.data}")

    while True:

        packed_op = simstate.data[simstate.ip]
        op = packed_op % 100

        if DEBUG:
            print("ip:", simstate.ip, 'op:', op, 'instr:',simstate.data[simstate.ip:simstate.ip+4])

        if op == 99:
            return "HALT"

        # ADD
        elif op == 1:
            a = _src_param(simstate, packed_op,  0)
            b = _src_param(simstate, packed_op,  1)
            _write_param(simstate, packed_op, 2, a+b)
            simstate.ip += 4

        # MULT
        elif op == 2:
            a = _src_param(simstate, packed_op,  0)
            b = _src_param(simstate, packed_op,  1)
            _write_param(simstate, packed_op, 2, a*b)

            simstate.ip += 4

        # INPUT
        elif op == 3:
            if len(simstate.input) <= 0:
                return 'INPUT'

            value = simstate.input.pop(0)
            _write_param(simstate, packed_op, 0, value)
            simstate.ip += 2

        # OUTPUT
        elif op == 4:
            a = _src_param(simstate, packed_op,  0)
            simstate.output.append(a)
            simstate.ip += 2
            return "OUTPUT"

        # jmp if != 0
        elif op == 5:
            a = _src_param(simstate, packed_op,  0)
            b = _src_param(simstate, packed_op,  1)

            if a != 0:
                simstate.ip = b
                assert(simstate.ip is not None)
            else:
                simstate.ip += 3

        # jmp if == 0
        elif op == 6:
            a = _src_param(simstate, packed_op,  0)
            b = _src_param(simstate, packed_op,  1)

            if a == 0:
                simstate.ip = b
                assert(simstate.ip is not None)
            else:
                simstate.ip += 3

        # a < b
        elif op == 7:
            a = _src_param(simstate, packed_op,  0)
            b = _src_param(simstate, packed_op,  1)

            if a < b:
                _write_param(simstate, packed_op, 2, 1)
            else:
                _write_param(simstate, packed_op, 2, 0)
            simstate.ip += 4

        # a == b
        elif op == 8:
            a = _src_param(simstate, packed_op,  0)
            b = _src_param(simstate, packed_op,  1)

            if a == b:
                _write_param(simstate, packed_op, 2, 1)
            else:
                _write_param(simstate, packed_op, 2, 0)
            simstate.ip += 4

        # adjust base
        elif op == 9:
            a = _src_param(simstate, packed_op,  0)
            simstate.base += a
            simstate.ip += 2

        else:
            raise Exception(f"[{simstate.name}] bad op: {op}")

    raise Exception(f"[{simstate.name}] unexpected exit")


# Example of wrapping intcode vm as a function

'''

class IntCodeFunction:

    def __init__(self, data):
        self.sim_state = SimState('func', data)
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


f = IntCodeFunction(data)
v = f(x,y)

'''