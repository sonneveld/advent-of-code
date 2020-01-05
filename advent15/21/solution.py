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
from collections import namedtuple
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import permutations
from itertools import product
from multiprocessing import Pool
from math import sqrt

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        hp, damage, armour = (int(x) for x in re.findall(r"\d+", f.read()))
        return hp, damage, armour


SHOP = '''Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3'''

WEAPONS = (
    # NOTE! must have a weapon

    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0),
)

ARMOUR = (
    (0, 0, 0), # NONE

    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5),
)

RINGS = (
    (0, 0, 0), # NONE
    (0, 0, 0), # NONE

    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
)

def part_1_2(data):

    boss_init_hp, boss_damage, boss_armour = data

    player_init_hp = 100

    ring_combos = list(combinations(RINGS, 2))

    win_costs = set()
    lose_costs = set()

    for weapon, armour, rings in itertools.product(WEAPONS, ARMOUR, ring_combos):
        ring_a, ring_b = rings

        cost = sum(x[0] for x in (weapon, armour, ring_a, ring_b))
        player_damage = sum(x[1] for x in (weapon, armour, ring_a, ring_b))
        player_armour = sum(x[2] for x in (weapon, armour, ring_a, ring_b))

        player_hp = player_init_hp
        boss_hp = boss_init_hp

        while True:
            # player attack
            damage_dealt = player_damage - boss_armour
            if damage_dealt < 1:
                damage_dealt = 1
            
            boss_hp -= damage_dealt
            if boss_hp <= 0:
                boss_hp = 0
                break

            # boss attack
            damage_dealt = boss_damage - player_armour
            if damage_dealt < 1:
                damage_dealt = 1

            player_hp -= damage_dealt
            if player_hp <= 0:
                player_hp = 0
                break

        assert player_hp != boss_hp
        if player_hp > boss_hp:
            print (cost, player_damage, player_armour, ' \t', (weapon, armour, ring_a, ring_b), ' \t', f"hp:{player_hp} bosshp:{boss_hp}  \tPLAYER WINS")
            win_costs.add(cost)
        else:
            print (cost, player_damage, player_armour, ' \t', (weapon, armour, ring_a, ring_b), ' \t', f"hp:{player_hp} bosshp:{boss_hp}  \tBOSS WINS")
            lose_costs.add(cost)

    return min(win_costs), max(lose_costs)


def main():
    data = load()
    p1,p2 = part_1_2(data)
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
