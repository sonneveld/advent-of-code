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
from itertools import combinations, permutations, product, count, cycle, islice
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
            row = tuple(int(x) for x in re.findall(r'\-?\d+', l))
            data.append(row)
        return data


# ---------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------

def part_1(data):

    plist = []
    vlist = []
    alist = []

    for px, py, pz, vx, vy, vz, ax, ay, az in data:
        plist.append( (px, py, pz) )
        vlist.append( (vx, vy, vz) )
        alist.append( (ax, ay, az) )

    result = None

    for _ in range(512):

        for i in range(len(data)):
            p = plist[i]
            v = vlist[i]
            a = alist[i]

            new_v = (v[0]+a[0], v[1]+a[1], v[2]+a[2])
            new_p = (p[0]+new_v[0], p[1]+new_v[1], p[2]+new_v[2])

            plist[i] = new_p
            vlist[i] = new_v

        mdlist = [ abs(p[0]) + abs(p[1]) + abs(p[2]) for p in plist]
        min_md = min(mdlist)
        result = mdlist.index(min_md)

    return result

# ---------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------

def part_2(data):
    plist = []
    vlist = []
    alist = []

    for px, py, pz, vx, vy, vz, ax, ay, az in data:
        plist.append( (px, py, pz) )
        vlist.append( (vx, vy, vz) )
        alist.append( (ax, ay, az) )

    result = None

    for _ in range(64):

        # delete sameys

        to_delete = set()
        pcount = Counter(plist)
        for p, ammt in pcount.most_common():
            if ammt > 1:
                to_delete.add(p)

        new_plist = []
        new_vlist = []
        new_alist = []

        for i in range(len(plist)):
            p = plist[i]
            if p in to_delete:
                continue
            v = vlist[i]
            a = alist[i]

            new_plist.append(p)
            new_vlist.append(v)
            new_alist.append(a)

        plist = new_plist
        vlist = new_vlist
        alist = new_alist

        # update positions

        for i in range(len(plist)):
            p = plist[i]
            v = vlist[i]
            a = alist[i]

            new_v = (v[0]+a[0], v[1]+a[1], v[2]+a[2])
            new_p = (p[0]+new_v[0], p[1]+new_v[1], p[2]+new_v[2])

            plist[i] = new_p
            vlist[i] = new_v

        result = len(plist)

    return result



def main():
    data = load()

    p1 = part_1(data)
    print(p1)

    p2 = part_2(data)
    print(p2)


if __name__ == "__main__":
    main()
