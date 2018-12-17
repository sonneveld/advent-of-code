#!/usr/bin/env python3

import re
import collections
import sys

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    data = [x.strip() for x in f.readlines()]


ground = {}

for line in data:
    if line[0] == 'x':
        x, y1, y2 = [int(x) for x in re.findall(r'\d+', line)]
        for y in range(y1, y2+1):
            ground[(x,y)] = "#"
    if line[0] == 'y':
        y, x1, x2 = [int(x) for x in re.findall(r'\d+', line)]
        for x in range(x1, x2+1):
            ground[(x,y)] = "#"

x_min = min(key[0] for key in ground.keys())
x_max = max(key[0] for key in ground.keys())
y_min = min(key[1] for key in ground.keys())
y_max = max(key[1] for key in ground.keys())

ground[(500,0)] = "+"


def dump():

    for y in range(y_min-10, y_max+10):
        print (f"y={y:04}", end='')
        for x in range(x_min-10, x_max+10):
            print (ground.get((x,y), " "), end = '')
        print()

def is_wall(pos):
    ground_ch = ground.get(pos, '.')
    return ground_ch == "#"

def has_hole(pos):
    underneath_pos = ( pos[0],  pos[1] + 1 )
    underneath_ch = ground.get(underneath_pos, '.')
    return underneath_ch not in  "#~"

def find_walls(from_pos):

    pos = from_pos
    while True:
        ground_ch = ground.get(pos, '.')
        underneath_ch = ground.get((pos[0], pos[1]+1), '.')
        if ground_ch == "#":
            break
        if underneath_ch not in "#~":
            break
        pos = (pos[0]-1, pos[1])
    start_pos = pos

    pos = from_pos
    while True:
        ground_ch = ground.get(pos, '.')
        underneath_ch = ground.get((pos[0], pos[1]+1), '.')
        if ground_ch == "#":
            break
        if underneath_ch not in "#~":
            break
        pos = (pos[0]+1, pos[1])
    end_pos = pos

    return (start_pos, end_pos)


seen = set()
work_queue = [(500, 0)]

while len(work_queue) > 0:

    start_pos = work_queue.pop()
    seen.add(start_pos)
    x,y = start_pos

    # water stream down
    for y in range(start_pos[1], y_max+10):
        pos = (x,y)
        ground_ch = ground.get(pos, '.')
        if ground_ch == '.':
            ground[pos] = "|"
        if ground_ch == "#":
            break

    fill_pos = (pos[0], pos[1]-1)

    # fill from bottom
    reached_top = False
    while not reached_top:

        left_pos, right_pos = find_walls(fill_pos)

        ch = "~"

        if not is_wall(left_pos) and  has_hole(left_pos):
            ch = "|"
            reached_top = True
            if left_pos not in seen:
                work_queue.append(left_pos)

        if not is_wall(right_pos) and  has_hole(right_pos):
            ch = "|"
            reached_top = True
            if right_pos not in seen:
                work_queue.append(right_pos)

        pos = left_pos
        while True:
            ground_ch = ground.get(pos, '.')
            if ground_ch != "#":
                ground[pos] = ch

            if pos == right_pos:
                break

            pos = ( pos[0]+1, pos[1])

        fill_pos = (fill_pos[0], fill_pos[1]-1)



touched_values = []
wet_values = []
for p, v in ground.items():
    if p[1] > y_max:
        continue
    if p[1] < y_min:
        continue
    if v in "~":
        wet_values.append(v)
    if v in "~|":
        touched_values.append(v)

print (len(touched_values))
print (len(wet_values))
