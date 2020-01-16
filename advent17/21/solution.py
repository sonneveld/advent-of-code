#!/usr/bin/env python3

import sys
import os
import os.path
import re

import collections
import functools
import heapq
import itertools
import math
import multiprocessing
import random
import string
import time
import json
import hashlib

from collections import Counter, defaultdict, namedtuple, deque
from copy import copy, deepcopy
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, permutations, product, count, cycle, islice, chain
from multiprocessing import Pool
from math import sqrt


DEBUG = "DEBUG" in os.environ


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = []
        for l in f:
            l = l.strip()
            tokens = l.split(" => ")
            src = re.findall(r'[#\.]', tokens[0])
            dest = re.findall(r'[#\.]', tokens[1])
            data.append((src, dest))
        return data


class Bitmap:

    def __init__(self, width, height, data=None):

        self.width = width
        self.height = height
        if data is None:
            data = [None] * (width*height)
        assert len(data) == (width*height)
        self.data = data

    def get_pixel(self, x, y):
        return self.data[self.width*y + x]

    def set_pixel(self, x, y, v):
        self.data[self.width*y + x] = v

    def subbitmap(self, subx, suby, width, height):
        next_data = []
        for y in range(suby, suby+height):
            for x in range(subx, subx+width):
                next_data.append(self.get_pixel(x, y))
        return Bitmap(width, height, next_data)

    def rotate(self):
        next_data = []
        for x in range(self.width):
            for y in reversed(range(self.height)):
                next_data.append(self.get_pixel(x, y))
        return Bitmap(self.width, self.height, next_data)

    def flip_top_down(self):
        next_data = []
        for y in reversed(range(self.height)):
            for x in range(self.width):
                next_data.append(self.get_pixel(x, y))
        return Bitmap(self.width, self.height, next_data)

    def flip_left_right(self):
        next_data = []
        for y in range(self.height):
            for x in reversed(range(self.width)):
                next_data.append(self.get_pixel(x, y))
        return Bitmap(self.width, self.height, next_data)

    def blit(self, to_x, to_y, otherbmp):
        for y in range(otherbmp.height):
            for x in range(otherbmp.width):
                self.set_pixel(to_x+x, to_y+y, otherbmp.get_pixel(x, y))

    def dump(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.get_pixel(x,y), end='')
            print()


def bmp_variants(in_bmp):

    yield in_bmp

    b = in_bmp.rotate()
    yield b
    b = b.rotate()
    yield b
    b = b.rotate()
    yield b

    b = in_bmp.flip_left_right()
    yield b
    b = b.rotate()
    yield b
    b = b.rotate()
    yield b
    b = b.rotate()
    yield b

    b = in_bmp.flip_top_down()
    yield b
    b = b.rotate()
    yield b
    b = b.rotate()
    yield b
    b = b.rotate()
    yield b


def enhance2(transforms_2, in_bmp):

    IN_SIZE = 2
    OUT_SIZE = 3

    out_bmp = Bitmap(in_bmp.width // IN_SIZE * OUT_SIZE, in_bmp.height // IN_SIZE * OUT_SIZE)

    for x,y in product(range(0, in_bmp.width, IN_SIZE), repeat=2):
        sub_bmp = in_bmp.subbitmap(x, y, IN_SIZE, IN_SIZE)

        transform_out = None
        for (src, dest), bmp in product(transforms_2, bmp_variants(sub_bmp)):
            if src == bmp.data:
                transform_out = dest
                break
        assert transform_out is not None

        dest_bmp = Bitmap(OUT_SIZE, OUT_SIZE, transform_out)

        out_bmp.blit(x // IN_SIZE * OUT_SIZE, y // IN_SIZE * OUT_SIZE, dest_bmp)

    return out_bmp

def enhance3(transforms_3, in_bmp):

    IN_SIZE = 3
    OUT_SIZE = 4

    out_bmp = Bitmap(in_bmp.width // IN_SIZE * OUT_SIZE, in_bmp.height // IN_SIZE * OUT_SIZE)

    for x,y in product(range(0, in_bmp.width, IN_SIZE), repeat=2):
        sub_bmp = in_bmp.subbitmap(x, y, IN_SIZE, IN_SIZE)

        transform_out = None
        for (src, dest), bmp in product(transforms_3, bmp_variants(sub_bmp)):
            if src == bmp.data:
                transform_out = dest
                break
        assert transform_out is not None

        dest_bmp = Bitmap(OUT_SIZE, OUT_SIZE, transform_out)

        out_bmp.blit(x // IN_SIZE * OUT_SIZE, y // IN_SIZE * OUT_SIZE, dest_bmp)

    return out_bmp


def solution(data, num_iterations):

    transforms_2 = [ x for x in data if len(x[0]) == 2*2]
    transforms_3 = [ x for x in data if len(x[0]) == 3*3]
    
    basebmp = Bitmap(3, 3, list('.#...####') )

    # print()
    # basebmp.dump()

    for iteration in range(num_iterations):
        print (iteration, basebmp.width, 'x', basebmp.height)

        assert basebmp.width == basebmp.height

        if basebmp.width % 2 == 0:
            basebmp = enhance2(transforms_2, basebmp)
        elif basebmp.width % 3 == 0:
            basebmp = enhance3(transforms_3, basebmp)
        else:
            raise Exception(f'bad size: {basebmp.width}')

        # print()
        # basebmp.dump()

    return basebmp.data.count("#")


def part_1(data):
    return solution(data, 5)

def part_2(data):
    return solution(data, 18)


def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
