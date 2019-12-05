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


def read_val(data, params, param_off, val_in):

    val = None
    if params[param_off] == 0:  # position
        val = data[val_in]
    elif params[param_off] == 1:  # position
        val = val_in
    else:
        raise Exception(f"unknown param: {params[param_off]}")

    return val

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

    while True:
        instr_ip = ip


        op = data[ip]
        ip += 1


        params = []
        parameter = op // 100
        for x in range(4):
            params.append(parameter % 10)
            parameter //= 10

        op = op % 100


        if DEBUG:
            print("op", op)

        if op == 99:
            break
    
        elif op == 1:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1
            c = data[ip]
            ip += 1
            if DEBUG:
                print('add',a,b,c)


            a_val = None
            if params[0] == 0:  # position
                a_val = data[a]
            elif params[0] == 1:  # position
                a_val = a
            else:
                raise Exception(f"unknown param: {params[0]}" )

            b_val = None
            if params[1] == 0:  # position
                b_val = data[b]
            elif params[1] == 1:  # position
                b_val = b
            else:
                raise Exception(f"unknown param: {params[1]}" )

            data[c] = a_val + b_val

        elif op == 2:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1
            c = data[ip]
            ip += 1
            if DEBUG:
                print('mul',a,b,c)

            a_val = None
            if params[0] == 0:  # position
                a_val = data[a]
            elif params[0] == 1:  # position
                a_val = a
            else:
                raise Exception(f"unknown param: {params[0]}" )


            b_val = None
            if params[1] == 0:  # position
                b_val = data[b]
            elif params[1] == 1:  # position
                b_val = b
            else:
                raise Exception(f"unknown param: {params[1]}" )

            data[c] = a_val * b_val
    
        elif op == 3:

            a = data[ip]
            ip += 1

            value = input("input: ")
            value = int(value)

            data[a] = value

        elif op == 4:
            a = data[ip]
            ip += 1

            a_val = None
            if params[0] == 0:  # position
                a_val = data[a]
            elif params[0] == 1:  # position
                a_val = a

            print(a_val)

        elif op == 5:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1

            a_val = read_val(data, params, 0, a)
            b_val = read_val(data, params, 1, b)

            if a_val != 0:
                ip = b_val

            assert(ip is not None)

        elif op == 6:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1

            a_val = read_val(data, params, 0, a)
            b_val = read_val(data, params, 1, b)

            if a_val == 0:
                ip = b_val
            assert(ip is not None)

        elif op == 7:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1
            c = data[ip]
            ip += 1

            a_val = read_val(data, params, 0, a)
            b_val = read_val(data, params, 1, b)
            c_val = read_val(data, params, 2, c)

            if a_val < b_val:
                data[c] = 1
            else:
                data[c] = 0

        elif op == 8:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1
            c = data[ip]
            ip += 1

            a_val = read_val(data, params, 0, a)
            b_val = read_val(data, params, 1, b)
            c_val = read_val(data, params, 2, c)

            if a_val == b_val:
                data[c] = 1
            else:
                data[c] = 0

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