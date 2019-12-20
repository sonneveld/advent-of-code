#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import Counter
import math
import multiprocessing
from multiprocessing import Pool

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.readline().strip()
        data = [int(x) for x in data]
        return data



base_pattern = [0, 1, 0, -1]

def base_generator(offset):
    skip = True
    multiple = offset+1
    while True:
        for b in base_pattern:
            for x in range(multiple):
                if not skip:
                    yield b
                skip = False

def dump_base_pattern():
    for offset in range(70):
        print("%2d"%offset, end="    ")
        count = 70
        for x in base_generator(offset):
            print("%2d"%x, end=' ')
            count -= 1
            if count <= 0:
                break
        print()


# ------------------------------------------------------------------------------------------------------------------
# PART ONE
# ------------------------------------------------------------------------------------------------------------------

def fft_offset(x):
    offset, data = x
    value = sum( x*y for x,y in zip(data, base_generator(offset)))
    value = abs(value) % 10
    return value

def fft_pool(data, pool):
    return pool.map(fft_offset, ( (x,data) for x in range(len(data)))  )

def fft_slow(data):
    result = []
    for offset in range(len(data)):
        value = sum( x*y for x,y in zip(data, base_generator(offset)))
        value = abs(value) % 10
        result.append(value)
    return result

def part_1(data):
    USE_POOL=True

    if USE_POOL:
        with Pool(9) as p:
            for x in range(100):
                data = fft_pool(data, p)
    else:
        for x in range(100):
            data = fft_slow(data)

    return data[:8]


# ------------------------------------------------------------------------------------------------------------------
# PART TWO
# ------------------------------------------------------------------------------------------------------------------

def part_2(data):

    offset = data[0] * 1000000 + data[1] * 100000 + data[2] * 10000 + data[3] * 1000 + data[4] * 100 + data[5] * 10 + data[6] * 1
    data = data*10000

    if False:
        print('input', data)
        print("offset", offset)
        print('input', len(data))

    # THIS is the trick, only works for offsets in second half
    assert (offset > len(data)//2)

    for phase in range(100):

        new_data = [0]*len(data)
        for x in reversed(range(offset, len(data))):
            if x+1 == len(data):
                new_data[x] = abs(data[x])%10
            else:
                new_data[x] = abs(data[x] + new_data[x+1])%10

        data = new_data

    return list(abs(x)%10 for x in data[offset:offset+8])


def main():
    data = load()

    if True:
        dump_base_pattern()

    value = part_1(data)
    print(''.join(str(x) for x in value))

    value = part_2(data)
    print(''.join(str(x) for x in value))


if __name__ == "__main__":
    main()