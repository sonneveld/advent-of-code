#!/usr/bin/env python3

import sys
import os
import os.path
import re
from collections import defaultdict
from functools import lru_cache

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    data = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            obj,orbiter = line.split(")")
            data.append( (obj,orbiter) )
    return data


def part_1(data):

    @lru_cache(None)
    def find_parent(wanted_orbiter):
        for search_obj, search_orbiter in data:
            if search_orbiter == wanted_orbiter:
                return search_obj
        return None

    objects = set()

    for obj,orbiter in data:
        objects.add(obj)
        objects.add(orbiter)

    orbit_count = 0

    for obj in objects:
        c = obj
        while c is not None:
            c = find_parent(c)
            if c != None:
                orbit_count += 1

    return orbit_count


def part_2(data):

    @lru_cache(None)
    def find_parent(wanted_orbiter):
        for search_obj, search_orbiter in data:
            if search_orbiter == wanted_orbiter:
                return search_obj
        return None

    you_orbit = find_parent('YOU')
    santa_orbit = find_parent('SAN')

    search_set = set([santa_orbit,])

    transfer_count = 0

    while True:
        new_set = set()

        for obj,orbiter in data:
            if obj in search_set or orbiter in search_set:
                new_set.add(obj)
                new_set.add(orbiter)

        search_set |= new_set

        transfer_count += 1

        if you_orbit in search_set:
            break

    return transfer_count


def main():
    data = load()

    result = part_1(data)
    print(result)

    result = part_2(data)
    print(result)


if __name__ == "__main__":
    main()
