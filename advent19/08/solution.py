#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import Counter

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.readline().strip()
        data = [int(x) for x in data]
        return data


def part_1(data):
    layer_size = 25 * 6
    layers = []

    i = 0
    while i < len(data):
        layer = data[i: i+layer_size]
        count = Counter(layer)
        layers.append( [count[0], count[1] * count[2]] )
        i += layer_size
    
    layers.sort()
    return layers[0][1]


def part_2(data):

    layer_size = 25 * 6
    layers = []

    i = 0
    while i < len(data):
        layer = data[i: i+layer_size]
        layers.append(layer)
        i += layer_size

    output = layers[-1]

    for layer in reversed(layers[:-1]):

        new_out = []
        for bottom, top in zip(output, layer):
            val = bottom
            if top != 2:
                val = top
            new_out.append(val)

        output = new_out

    pixel_map = {
        1 : "X",
        0 : " ",
        2 : "?"
    }

    for y in range(6):

        row = output[y*25: y*25+25]
        row = [pixel_map[x] for x in row]

        print (''.join(row))


def main():
    data = load()

    value = part_1(data)
    print(value)

    part_2(data)


if __name__ == "__main__":
    main()
