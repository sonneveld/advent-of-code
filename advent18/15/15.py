import re
import collections
import sys
import os

DEBUG = "DEBUG" in os.environ

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"


with open(input_filename) as f:
    data = [x.strip() for x in f.readlines()]

dump_width = len(data[0])
dump_height = len(data)



def dump(floor, entities):

    for y in range(dump_height):
        seen = []

        for x in range(dump_width):
            elist = [e for e in entities if e.x == x and e.y == y]
            if len(elist) > 0:
                e = elist[0]
                print(elist[0].char, end = '')
                seen.append(f"{e.char}[{e.hp}]")

            elif (x,y) in floor:
                print(floor[(x,y)], end='')
            else:
                print(' ', end='')
        print("   ", " ".join(seen))


def dump_distance_info(distance_info):
    for y in range(dump_height):
        for x in range(dump_width):
            pos = (x,y)
            if pos in distance_info:
                print(f"{distance_info[pos]:02} ", end='')
            else :
                print ("   ", end='')
        print()

def dump_path(distance_info, path):

    for y in range(dump_height):
        for x in range(dump_width):
            pos = (x,y)
            if pos in path:
                print(f"XX ", end='')
            elif pos in distance_info:
                print(f"{distance_info[pos]:02} ", end='')
            else :
                print ("   ", end='')
        print()




def reachable_pos(x,y):
    return set(
        [(x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)]
    )

def adjacent_squares(floor, entities, enemies):
    open_squares = set(k for k,v in floor.items() if v == '.')
    entity_poses = set( (e.x, e.y) for e in entities )
    open_squares -= entity_poses  # positions that don't have an entity on them

    adjacent_poses = set()
    for e in enemies:
        adjacent_poses |= reachable_pos(e.x, e.y)

    return open_squares.intersection(adjacent_poses)


''' return distance to all available points '''
def get_distance_info(floor, entities, entity):
    available_squares = set(k for k,v in floor.items() if v == '.') -  set( (e.x, e.y) for e in entities )
    info = {}
    distance = 0
    queue = set([ (entity.x, entity.y) ])

    while len(queue) > 0:

        for pos in queue:
            info[pos] = distance
            if pos in available_squares:
                available_squares.remove(pos)

        distance += 1

        new_queue = set()
        for entry in queue:
            new_queue |=  set(reachable_pos(entry[0], entry[1])) & available_squares
        queue = new_queue

    return info


def get_path(pos_from, pos_to, distance_info):

    path = [pos_to]
    dist = distance_info[pos_to]

    while pos_from not in path:
        next_reachable = set()
        for pos in path:
            next_reachable |=  set(  n for n in reachable_pos(pos[0], pos[1]) if n in distance_info and distance_info[n] < dist  )

        next_reachable = list(next_reachable)
        next_reachable.sort(key= lambda p : (p[1], p[0]))
        path = next_reachable + path

        dist -= 1

    return path[1:]



class Elf(object):
    def __init__(self, x, y, attack_power):
        self.x = x
        self.y = y
        self.dead = False
        self.char = "E"
        self.hp = 200
        self.attack_power = attack_power
        self.last_round = None
    def __str__(self):
        return f"{self.char}[{self.x},{self.y}]"

class Goblin(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dead = False
        self.char = "G"
        self.hp = 200
        self.attack_power = 3
        self.last_round = None
    def __str__(self):
        return f"{self.char}[{self.x},{self.y}]"


def simulate(elf_attack_power):

    all_entities = []
    floor = {}

    for y,row in enumerate(data):
        for x,col in enumerate(row):
            if col == "E":
                all_entities.append( Elf(x,y, elf_attack_power) )
                floor[(x,y)] = '.'
            elif col == "G":
                all_entities.append( Goblin(x,y) )
                floor[(x,y)] = '.'
            elif col in ".#":
                floor[(x,y)] = col


    entities = all_entities
    last_full_round = None
    round = 1

    while True:

        if DEBUG:
            print()
            print("-----------------------------------------------------------")
            print(f"elf_attack_power={elf_attack_power} round={round}")
            print("-----------------------------------------------------------")

            dump(floor, entities)

        entities_in_process_order = list(entities)
        entities_in_process_order.sort(key = lambda e: (e.y, e.x) )

        for entity in entities_in_process_order:

            if entity.dead:
                continue

            entity_id = f"{entity}"
            entity_events = []

            enemies = [x for x in entities if x.__class__ != entity.__class__]

            if len(enemies) > 0:
                entity.last_round = round

            moved = False

            enemies_in_attack_range = [ e for e in enemies if (e.x,e.y) in reachable_pos(entity.x, entity.y)]
            if len(enemies_in_attack_range) == 0:
                # move if nothing in range
                distance_info = get_distance_info(floor, entities, entity)
                adj_squares = adjacent_squares(floor, entities, enemies)
                destinations = []
                for p in adj_squares:
                    if p in distance_info:
                        destinations.append( (distance_info[p],p) )

                destinations.sort(key= lambda entry:( entry[0], entry[1][1], entry[1][0]))
                destinations = destinations[:1]
                if len(destinations) == 1:
                    pos_from = (entity.x, entity.y)
                    pos_to = destinations[0][1]
                    path = get_path(pos_from, pos_to, distance_info)
                    pos_next = path[0]
                    entity_events.append(f"moving to {pos_next}")
                    entity.x = pos_next[0]
                    entity.y = pos_next[1]
                    moved = True

            if not moved:
                entity_events.append("stationary")


            enemies_in_attack_range = [ e for e in enemies if (e.x,e.y) in reachable_pos(entity.x, entity.y)]
            if len(enemies_in_attack_range) > 0:
                enemies_in_attack_range.sort(key= lambda e: (e.hp, e.y, e.x))
                to_attack = enemies_in_attack_range[0]
                to_attack.hp -= entity.attack_power
                to_attack.dead = (to_attack.hp <= 0)
                entities = [e for e in entities if not e.dead]

                entity_events.append(f"attack {to_attack}")
            else:
                entity_events.append("attack nothing")

            # double check we're not walking over people
            pos_set = set( [  (e.x, e.y) for e in entities   ]  )
            assert(len(pos_set) == len(entities))

            if DEBUG:
                print(f"{entity_id}: {', '.join(entity_events)}")


        if DEBUG:
            dump(floor, entities)

        if all(e.dead or e.last_round == round for e in entities):
            last_full_round = round

        # one race is dead.
        entity_classes = set( x.__class__ for x in entities if not x.dead )
        if len(entity_classes) == 1:
            break

        round += 1

    return last_full_round, all_entities


# Part 1

last_full_round, entities = simulate(3)
e_sum = sum(e.hp for e in entities if not e.dead)
print(e_sum * last_full_round)



# Part 2

elf_attack_power = 3

for elf_attack_power in range(3, 100):

    elf_attack_power += 1

    last_full_round, entities = simulate(elf_attack_power)

    dead_elves = [e for e in entities if isinstance(e, Elf) and e.dead]
    if len(dead_elves) == 0:
        e_sum = sum(e.hp for e in entities if not e.dead)
        print(e_sum * last_full_round)
        break
