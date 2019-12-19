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
        for line in f:
            line = line.strip()
            tokens = line.split()
            data.append( (tokens[0], tokens[2], int(tokens[4])))
        return data



def part_1(data):

    places = set()

    distance_by = {}

    for left, right, dist in data:
        places.add(left)
        places.add(right)
        k= frozenset((left, right))
        distance_by[k] = dist

    
    results = set()
    for path in permutations(places):

        distance = 0
        prev = None
        for p in path:
            if prev is not None:
                k= frozenset((prev, p))
                distance += distance_by[k]
            prev = p

        results.add(distance)
    
    return results




def main():
    data = load()
    results = part_1(data)
    print(min(results))
    print(max(results))


if __name__ == "__main__":
    main()
