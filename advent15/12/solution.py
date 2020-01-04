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

from collections import Counter
from collections import defaultdict
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import product
from multiprocessing import Pool


DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    result = []
    with open(filename) as f:
        data = f.read()
        return data


def part_1(data):
    answer = re.findall(r"\-?\d+", data)
    return sum( int(x) for x in answer) 

def part_2(data):

    def no_reds(o):
        for k,v in o.items():
            if v == 'red':
                return None
        return o

    data = json.loads(data, object_hook=no_reds)
    data = json.dumps(data)
    answer = re.findall(r"\-?\d+", data)
    return sum( int(x) for x in answer) 
       

def main():
    data = load()
    p1 = part_1(data)
    p2 = part_2(data)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
