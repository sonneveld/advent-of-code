#!/usr/bin/env python3

import re
import collections
import sys
import os
from heapq import heappush, heappop
from functools import lru_cache
import random

sys.setrecursionlimit(2000)

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

data = []

class Group(object):
    def __init__(self, group_id, team, units, hit_points, attack_damage, attack_type, initiative, weaknesses, immunities):
        self.group_id = group_id
        self.team = team
        self.units = units
        self.hit_points = hit_points
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def __repr__(self):
        return (f"{self.team}:{self.group_id}  units:{self.units}, hp: {self.hit_points}, attack: {self.attack_damage}, at: {self.attack_type}, init: {self.initiative}, weak: {self.weaknesses}, immun:{self.immunities}")

def group_effective_power(group):
    assert group.units > 0
    return group.units * group.attack_damage

def calc_damage(attacking_group, defending_group):
    damage = group_effective_power(attacking_group)
    if attacking_group.attack_type in defending_group.immunities:
        return 0
    elif attacking_group.attack_type in defending_group.weaknesses:
        return damage * 2
    else:
        return damage

def parse_line(group_id, team, line):
    m = re.search(r'(\d+) unit', line)
    assert m is not None
    units = int(m.group(1))

    m = re.search(r'(\d+) hit points', line)
    assert m is not None
    hit_points = int(m.group(1))

    weaknesses = set()
    immunities = set()

    if '(' in line:
        m = re.search(r'\((.*)\)', line)
        assert m is not None
        details = m.group(1)
        details = [x.strip() for x in details.split(';')]
        for entry in details:
            tokens = re.findall(r'\w+', entry)
            weakimmun = tokens[0]
            weakimmun_type = tokens[2:]
            if weakimmun == 'weak':
                weaknesses.update(tokens[2:])
            elif weakimmun == 'immune':
                immunities.update(tokens[2:])
            else:
                raise Exception()

    m = re.search(r'with an attack that does (\d+) (\w+) damage at initiative (\d+)', line)
    assert m is not None
    attack_damage = int(m.group(1))
    attack_type = m.group(2)
    initiative = int(m.group(3))

    return Group(group_id, team, units, hit_points, attack_damage, attack_type, initiative, weaknesses, immunities)



def run_simulation(boost=0):

    if DEBUG:
        print()
        print()
        print ('---------------------------------------------------------------------------------------------------------')
        print ('boost', boost)
        print ('---------------------------------------------------------------------------------------------------------')


    all_groups = []

    with open(input_filename) as f:
        data = [x.strip() for x in f.readlines()]
        for line in data:
            if len(line) <= 0:
                continue
            if line == 'Immune System:':
                team = 'immune'
                i = 1
            elif line == 'Infection:':
                team = 'infection'
                i = 1
            else:
                g = parse_line(i, team, line)
                if team == "immune":
                    g.attack_damage +=  boost
                all_groups.append(g)
                i += 1


    groups = all_groups

    round = 1
    while True:
        if DEBUG:
            print()
            print()
            print ('------------------------------------------------')
            print ('round', round)
            print ('------------------------------------------------')


        # target selection

        groups.sort(key = lambda g: (group_effective_power(g), g.initiative) , reverse = True)

        if DEBUG:
            for g in groups:
                print (g.team, g.group_id, g.units, 'effective power', group_effective_power(g), g.initiative)
                assert(g.units > 0)
            print()


        attack_pairings = []
        attacked = set()

        if DEBUG:
            print("* target selection")

        attack_order = list(groups)
        attack_order.sort(key = lambda g: (group_effective_power(g), g.initiative) , reverse = True)

        attack_count = collections.Counter(group_effective_power(g) for g in groups)
        most= (attack_count.most_common(1))[0]

        for attacking_group in attack_order:
            if DEBUG:
                print('  - attacking group: ', attacking_group)
            defending_groups = []
            for defending_group in groups:
                if defending_group in attacked:
                    continue
                if defending_group.team == attacking_group.team:
                    continue
                damage = calc_damage(attacking_group, defending_group)
                if damage > 0:
                    defending_groups.append( (damage, group_effective_power(defending_group), defending_group.initiative, defending_group))

            defending_groups.sort(reverse=True)
            if DEBUG:
                for d in defending_groups:
                    print('      defending:',d)

            # print('num to attack', len(defending_groups))

            if len(defending_groups) > 0:
                damage, _, _, defending_group = defending_groups[0]
                attack_pairings.append((attacking_group,defending_group))
                attacked.add(defending_group)
                if DEBUG:
                    print('    selected', defending_group)

        assert len(attack_pairings) == len(attacked)


        # attacking
        if DEBUG:
            print()
            print('* attacking')
        attack_pairings.sort(key= lambda p: p[0].initiative, reverse=True )
        for attacking_group, defending_group in attack_pairings:
            if DEBUG:
                print ("  - attacking", attacking_group)
                print ("    defending", defending_group)
            assert defending_group.units > 0

            if attacking_group.units <= 0:
                continue
            damage = calc_damage(attacking_group, defending_group)
            units_killed = damage // defending_group.hit_points
            if units_killed > defending_group.units:
                units_killed = defending_group.units

            if DEBUG:
                print ("     ", units_killed, 'units killed')
            defending_group.units -= units_killed

        groups_alive = [g for g in groups if g.units > 0]
        teams_alive = set(g.team for g in groups_alive)
        groups = groups_alive

        if len(teams_alive) < 2:
            break

        round += 1

        if round > 5000:
            return (None, None)


    team_alive = list(teams_alive)[0]
    total_units = sum(g.units for g in groups)
    return (team_alive, total_units)



# part 1
team_alive, total_units = run_simulation()
print (total_units)


boost = 1
while True:
    team_alive, total_units = run_simulation(boost)
    if team_alive == "immune":
        break
    boost += 1

print (total_units)
