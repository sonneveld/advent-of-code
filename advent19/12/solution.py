#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import Counter
import math
from dataclasses import dataclass
from itertools import combinations
import functools

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    data = []
    with open(filename) as f:
        for line in f:
            data.append([int(x) for x in re.findall(r'\-?\d+', line)])
    return data


@dataclass
class Moon:
    x: int
    y: int
    z: int
    v_x : int = 0
    v_y : int = 0
    v_z : int = 0


# -------------------------------------------------------------------------------------------------------------------
# PART ONE
# -------------------------------------------------------------------------------------------------------------------

def part_1(data):

    moonz = []

    for x,y,z in data:
        moonz.append(Moon(x,y,z))

    steps = 0
    while True:
        if False:
            print()
            print(f'after {steps} steps')
            for moon in moonz:
                print(moon)

        energy = 0
        for moon in moonz:
            potential_en = abs(moon.x) + abs(moon.y) + abs(moon.z)
            kin_en = abs(moon.v_x) + abs(moon.v_y) + abs(moon.v_z)
            energy += potential_en * kin_en

        if False:
            print('energy', energy)

        if steps == 1000:
            return energy

        for a,b in combinations(moonz, 2):
            # print(a, b)
            if a.x != b.x:
                if a.x > b.x:
                    a.v_x -= 1
                    b.v_x += 1
                else:
                    a.v_x += 1
                    b.v_x -= 1

            if a.y != b.y:
                if a.y > b.y:
                    a.v_y -= 1
                    b.v_y += 1
                else:
                    a.v_y += 1
                    b.v_y -= 1

            if a.z != b.z:
                if a.z > b.z:
                    a.v_z -= 1
                    b.v_z += 1
                else:
                    a.v_z += 1
                    b.v_z -= 1

        for moon in moonz:
            moon.x += moon.v_x
            moon.y += moon.v_y
            moon.z += moon.v_z


        steps += 1


# -------------------------------------------------------------------------------------------------------------------
# PART TWO
# -------------------------------------------------------------------------------------------------------------------

# similar to part1 but we just generate a row of data, instead of moon objects
def moon_data_generator(data):

    moonz = []


    for x,y,z in data:
        moonz.append(Moon(x,y,z))

    steps = 0

    while True:

        row = []
        for moon in moonz:
            row.extend([moon.x, moon.y, moon.z, moon.v_x, moon.v_y, moon.v_z])

        yield (steps, row)

        for a,b in combinations(moonz, 2):
            if a.x != b.x:
                if a.x > b.x:
                    a.v_x -= 1
                    b.v_x += 1
                else:
                    a.v_x += 1
                    b.v_x -= 1

            if a.y != b.y:
                if a.y > b.y:
                    a.v_y -= 1
                    b.v_y += 1
                else:
                    a.v_y += 1
                    b.v_y -= 1

            if a.z != b.z:
                if a.z > b.z:
                    a.v_z -= 1
                    b.v_z += 1
                else:
                    a.v_z += 1
                    b.v_z -= 1

        for moon in moonz:
            moon.x += moon.v_x
            moon.y += moon.v_y
            moon.z += moon.v_z

        steps += 1


def find_sequence(subset):
    for n in range(50000, len(subset)//2):
        latest = subset[-n:]
        prev = subset[-2*n:-n]
        assert len(latest) == len(prev)
        if latest == prev:
            return n
    return None


def get_sequence_lengths(data):

    SEQUENCE_SIZE=2

    NUM_COLUMNS = len(data) * 6

    history = [None]*NUM_COLUMNS
    for col in range(NUM_COLUMNS):
        history[col] = []

    history_size = 0


    result = {}

    def both_halves_equal(coldata):
        l = len(coldata)
        assert(l % 2 == 0)
        offset = l//2
        for x in range(l//2):
            if coldata[x] != coldata[offset+x]:
                return False
        return True

    for entry in moon_data_generator(data):
        steps = entry[0]

        # wait until settled
        if steps < 10000:
            continue

        for col, val in enumerate(entry[1]):
            history[col].append(val)
        history_size += 1

        if history_size == SEQUENCE_SIZE*2:
            for col in range(NUM_COLUMNS):
                if col in result:
                    continue

                colset = history[col]
                if both_halves_equal(colset):
                    if False:
                        print(f"FOUND col:{col} size:{SEQUENCE_SIZE}")
                    if col not in result:
                        result[col] = SEQUENCE_SIZE

            SEQUENCE_SIZE += 1

        
        if len(result) == NUM_COLUMNS:
            break

    if False:
        for k,v in sorted(result.items()):
            print(k, v)

    return set(result.values())

# Stolen from https://stackoverflow.com/a/147539/84262
def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a
def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)
def lcmm(*args):
    """Return lcm of args."""   
    return functools.reduce(lcm, args)


def part_2(data):
    seq_lengths = get_sequence_lengths(data)
    return lcmm(*seq_lengths)


def main():
    data = load()

    v = part_1(data)
    print(v)

    v = part_2(data)
    print(v)


if __name__ == "__main__":
    main()
