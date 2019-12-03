#!/usr/bin/env python3

import sys
import os
import os.path
import re
from collections import defaultdict

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    data = []
    with open(filename) as f:
        for line in f:
            tokens = re.findall(r'\w\d+', line)
            data.append(tokens)
    return data

def manhatten_dis(a_x, a_y, b_x, b_y):
    return abs(b_x - a_x) + abs(b_y - a_y)

def part_1(data):

    wires = []
    state = defaultdict(int)
    for wire in data:

        points = set()
        pos_x = 0
        pos_y = 0
        for vector in wire:
            if DEBUG:
                print (vector)
            direction = vector[0]
            distance = int(vector[1:])

            if direction == "U":
                while distance > 0:
                    pos_y -= 1
                    points.add( (pos_x, pos_y) )
                    distance -= 1

            elif direction == "D":
                while distance > 0:
                    pos_y += 1
                    points.add( (pos_x, pos_y) )
                    distance -= 1

            elif direction == "L":
                while distance > 0:
                    pos_x -= 1
                    points.add( (pos_x, pos_y) )
                    distance -= 1

            elif direction == "R":
                while distance > 0:
                    pos_x += 1
                    points.add( (pos_x, pos_y) )
                    distance -= 1
        wires.append(points)

    points = wires[0].intersection(wires[1])
    if DEBUG:
        print (points)

    md = [manhatten_dis(0,0, k[0], k[1]) for k in points]
    if DEBUG:
        print (md)

    return min(md)



def part_2(data):

    wires = []
    state = defaultdict(int)
    for wire in data:

        points = {}
        steps = 0
        pos_x = 0
        pos_y = 0
        for vector in wire:
            if DEBUG:
                print (vector)
            direction = vector[0]
            distance = int(vector[1:])

            if direction == "U":
                while distance > 0:
                    pos_y -= 1
                    steps += 1
                    points[(pos_x, pos_y)] = steps
                    distance -= 1

            elif direction == "D":
                while distance > 0:
                    pos_y += 1
                    steps += 1
                    points[(pos_x, pos_y)] = steps
                    distance -= 1

            elif direction == "L":
                while distance > 0:
                    pos_x -= 1
                    steps += 1
                    points[(pos_x, pos_y)] = steps
                    distance -= 1

            elif direction == "R":
                while distance > 0:
                    pos_x += 1
                    steps += 1
                    points[(pos_x, pos_y)] = steps
                    distance -= 1
        wires.append(points)

    wire_1_points = set(wires[0].keys())
    wire_2_points = set(wires[1].keys())

    points = wire_1_points.intersection(wire_2_points)
    if DEBUG:
        print (points)

    cd = [wires[0][k] + wires[1][k] for k in points]
    if DEBUG:
        print (cd)

    return min(cd)


def main():

    data = load()

    result = part_1(data)
    print(result)

    result = part_2(data)
    print(result)


if __name__ == "__main__":
    main()
