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
from collections import defaultdict

from functools import lru_cache

DEBUG=False

@dataclass
class Chemical:
    quantity: int
    name: str

@dataclass
class Reaction:
    input: list
    output: Chemical


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    data = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            left, right = line.split("=>")
            left = [x.strip() for x in left.split(",")]
            right = right.strip()

            left = [x.split() for x in left]
            left = [(int(x[0]), x[1]) for x in left]
            right = right.split()
            right = (  int(right[0]), right[1])

            right = Chemical(right[0], right[1])

            left = [Chemical(x[0], x[1]) for x in left]

            data.append(Reaction(left, right))

    return data


def calculate_fuel(data, wanted_fuel):
    @lru_cache(None)
    def find_reaction_that_creates(chem_name):

        for reaction in data:
            if reaction.output.name == chem_name:
                return reaction

        raise Exception(f"could not found {chem_name}")        

    MAX_ORE = 1000000000000

    inventory = defaultdict(int)
    inventory['ORE'] = MAX_ORE

    def execute_reaction(reaction):

        if False:
            print()
            print("executing ", reaction)

        # ensure ingredients

        while True:
            have_all = True

            for inchem in reaction.input:

                if inventory[inchem.name] < inchem.quantity:
                    r = find_reaction_that_creates(inchem.name)
                    execute_reaction(r)
                    have_all = False
            if have_all:
                break

        if False:
            print("BEFORE inventory", inventory)

        for inchem in reaction.input:
            inventory[inchem.name] -= inchem.quantity

        if False:
            print(" AFTER inventory", inventory)

        for k,v in inventory.items():
            assert v>= 0

        inventory[reaction.output.name] += reaction.output.quantity

    
    fr = find_reaction_that_creates("FUEL")

    while inventory['FUEL'] != wanted_fuel:
        execute_reaction(fr)

    if False:
        print(inventory)

    return MAX_ORE - inventory['ORE']

def part_1(data):
    ore = calculate_fuel(data, 1)
    return ore

def part_2(data):
    # TODO searching
    ore = calculate_fuel(data, 2509120)
    return 2509120

def main():
    data = load()

    value = part_1(data)
    print(value)

    value = part_2(data)
    print(value)


if __name__ == "__main__":
    main()
