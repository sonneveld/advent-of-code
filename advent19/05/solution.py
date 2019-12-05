#!/usr/bin/env python3

import sys
import os
import os.path
import re

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.readline()
        data = data.split(",")
        data = [int(x) for x in data]
        return data


def simulator(data):
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
        print("before", data)

    ip = 0
    packed_op = None

    def src_parameter(param_index):
        param_type = (packed_op // 100 // (10**param_index) ) % 10
        val = data[ip + 1 + param_index]

        if param_type == 0:
            return data[val]
        elif param_type == 1:
            return val
        # guessing at future param types
        # elif param_type == 2:
            # return ip + val
        else:
            raise Exception(f"unknown param type: {param_type}")

    def dest_parameter(param_index):
        if DEBUG:
            param_type = (packed_op // 100 // (10**param_index) ) % 10
            # assert(param_type == 0)
            if param_type != 0:
                print(f"ip:{ip} WARNING dest parameter is not position")
        val = data[ip + 1 + param_index]
        return val

    while True:

        packed_op = data[ip]
        op = packed_op % 100

        if DEBUG:
            print("ip:", ip, 'op:', op, 'instr:',data[ip:ip+4])

        if op == 99:
            break
    
        elif op == 1:
            a = src_parameter(0)
            b = src_parameter(1)
            c = dest_parameter(2)
            data[c] = a + b
            ip += 4

        elif op == 2:
            a = src_parameter(0)
            b = src_parameter(1)
            c = dest_parameter(2)
            data[c] = a * b
            ip += 4
    
        elif op == 3:
            a = dest_parameter(0)

            value = input("input: ")
            value = int(value)

            data[a] = value
            ip += 2

        elif op == 4:
            a = src_parameter(0)
            print(a)
            ip += 2

        elif op == 5:
            a = src_parameter(0)
            b = src_parameter(1)

            if a != 0:
                ip = b
                assert(ip is not None)
            else:
                ip += 3

        elif op == 6:
            a = src_parameter(0)
            b = src_parameter(1)

            if a == 0:
                ip = b
                assert(ip is not None)
            else:
                ip += 3

        elif op == 7:
            a = src_parameter(0)
            b = src_parameter(1)
            c = dest_parameter(2)

            if a < b:
                data[c] = 1
            else:
                data[c] = 0
            ip += 4

        elif op == 8:
            a = src_parameter(0)
            b = src_parameter(1)
            c = dest_parameter(2)

            if a == b:
                data[c] = 1
            else:
                data[c] = 0
            ip += 4

        else:
            raise Exception(f"bad op: {op}")

    if DEBUG:
        print("after", data)

    return data


def main():
    data = load()
    simulator(data)


if __name__ == "__main__":
    main()
