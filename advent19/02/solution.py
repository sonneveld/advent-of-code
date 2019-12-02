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

    while True:
        instr_ip = ip

        op = data[ip]
        ip += 1

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

            data[c] = data[a] + data[b]

        elif op == 22:
            a = data[ip]
            ip += 1
            b = data[ip]
            ip += 1
            c = data[ip]
            ip += 1
            if DEBUG:
                print('mul',a,b,c)

            data[c] = data[a] * data[b]
    
        else:
            raise Exception(f"bad op: {op}")

    if DEBUG:
        print("after", data)

    return data

    
def part_1(data):
    part_1_data = list(data)
    part_1_data[1] = 12
    part_1_data[2] = 2
    result = simulator(part_1_data)
    return result[0]

def part_2(data):
    for noun in range(100):
        for verb in range(100):
            part_2_data = list(data)
            part_2_data[1] = noun
            part_2_data[2] = verb
            result = simulator(part_2_data)
            if result[0] == 1969_07_20:
                return 100*noun+verb
    raise Exception("not found")

def main():

    data = load()

    result = part_1(data)
    print(result)

    result = part_2(data)
    print(result)


if __name__ == "__main__":
    main()
