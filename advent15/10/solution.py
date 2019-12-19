#!/usr/bin/env python3

import sys
import os
import os.path
# import re
# import itertools
# from collections import Counter
# import math
# from dataclasses import dataclass

from itertools import permutations

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    data = []

    with open(filename) as f:
        return f.readline().strip()




def process(data):

    buf = []

    for x in data:
        if len(buf) == 0:
            buf.append(x)
            continue

        if x != buf[0]:
            yield buf
            buf = []
        buf.append(x)
    
    if buf:
        yield buf



def process_loop(data, count):

    last_len = None

    for x in range(count):
        new_data = []

        for x in process(data):
            new_data.append(f"{len(x)}")
            new_data.append(f"{x[0]}")
        data = new_data

        last_len = len(data)

    return last_len


def part_1(data):
    return process_loop(data, 40)
def part_2(data):
    return process_loop(data, 50)


def main():
    data = load()
    v = part_1(data)
    print(v)
    v = part_2(data)
    print(v)


if __name__ == "__main__":
    main()
