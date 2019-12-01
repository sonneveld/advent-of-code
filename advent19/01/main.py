#!/usr/bin/env python3

import sys
import os
import os.path
import re

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        lines = [x.strip() for x in f.readlines()]
        data = []
        for l in lines:
            values = [int(x) for x in l.split()]
            data.append(values)

    return data


def fuel_1(mass):
    f = int(mass / 3 ) - 2
    return f

def fuel_2(mass):

    f = 0

    new_f = fuel_1(mass)
    while new_f >= 0:
        f += new_f
        new_f = fuel_1(new_f)

    return f
    
def main():

    data = load()

    # part one
    s = 0
    for values in data:
        mass = values[0]
        f = fuel_1(mass)
        s += f
    print(s)

    # part two
    s = 0
    for values in data:
        mass = values[0]
        f = fuel_2(mass)
        s += f
    print(s)




if __name__ == "__main__":
    main()