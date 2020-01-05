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

from copy import deepcopy

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        hp, damage = (int(x) for x in re.findall(r"\d+", f.read()))
        return hp, damage


SPELLS = "missile drain shield poison recharge".split()

SPELL_COSTS = {
    "missile": 53,
    "drain": 73,
    "shield": 113,
    "poison": 173,
    "recharge": 229,
}

SPELL_TIMER = {
    "shield": 6,
    "poison": 6,
    "recharge": 5,
}

PLAYER_INIT_HP = 50
PLAYER_INIT_MANA = 500

class GameState():

    def __init__(self, boss_hp, boss_damage, hard):

        self.hard = hard

        self.boss_hp = boss_hp
        self.boss_damage = boss_damage

        self.player_hp = PLAYER_INIT_HP
        self.player_mana = PLAYER_INIT_MANA
        self.player_armour = 0
        self.player_mana_spent = 0

        self.effects = {}
        self.effects['shield'] = 0
        self.effects['poison'] = 0
        self.effects['recharge'] = 0

    def update_effects(self):

        self.player_armour = 0
        if self.effects['shield'] > 0:
            self.player_armour = 7

        if self.effects['recharge'] > 0:
            self.player_mana += 101

        if self.effects['poison'] > 0:
            self.boss_hp -= 3

        for k,v in list(self.effects.items()):
            if v > 0:
                self.effects[k] -= 1

    def update(self, with_spell):

        # PLAYER

        if self.hard:
            self.player_hp -= 1
            if self.player_hp <= 0:
                self.player_hp = 0
                return "BOSS"

        self.update_effects()

        if self.boss_hp <= 0:
            self.boss_hp = 0
            return "PLAYER"

        self.player_mana -= SPELL_COSTS[with_spell]

        if self.player_mana < 0:
            self.player_mana = 0
            return "BOSS"

        self.player_mana_spent += SPELL_COSTS[with_spell]
        
        if with_spell in ('shield', 'recharge', 'poison'):
            if self.effects[with_spell] > 0:
                return "INVALID"
            self.effects[with_spell] = SPELL_TIMER[with_spell]
        elif with_spell == "missile":
            self.boss_hp -= 4
        elif with_spell == "drain":
            self.boss_hp -= 2
            self.player_hp += 2
        else:
            raise Exception(f"unknown spell:{with_spell}")

        if self.boss_hp <= 0:
            self.boss_hp = 0
            return "PLAYER"


        # BOSS

        self.update_effects()

        if self.boss_hp <= 0:
            self.boss_hp = 0
            return "PLAYER"

        attack_value = self.boss_damage - self.player_armour
        if attack_value <= 0:
            attack_value = 1
        self.player_hp -= attack_value

        if self.player_hp <= 0:
            self.player_hp = 0
            return "BOSS"

    def dump_state(self):
        print("hp", self.player_hp, "mana", self.player_mana, "boss", self.boss_hp, self.effects)


def game_simulator(data, hard=False):

    boss_init_hp, boss_damage = data

    win_costs = set()

    states = [GameState(boss_init_hp, boss_damage, hard)]

    while states:

        print('todo', len(states))

        next_states = []

        for state in states:
            for spell in SPELLS:

                next_state = deepcopy(state)

                winner = next_state.update(spell)
                
                if winner is not None:
                    if winner == "INVALID":
                        pass
                    elif winner == "PLAYER":
                        win_costs.add(next_state.player_mana_spent)
                    elif winner == "BOSS":
                        pass
                    else:
                        raise Exception("unknown winner", winner)
                    continue

                next_states.append(next_state)

        states = next_states

        if win_costs:
            break

    assert len(win_costs) > 0

    return min(win_costs)


def main():
    data = load()

    p1 = game_simulator(data)
    print(p1)
    p2 = game_simulator(data, True)
    print(p2)


if __name__ == "__main__":
    main()
