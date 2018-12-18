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

cdata = []
for entry in data:
    coords = [int(x) for x in re.findall(r'[\-\+]?[\d]+', entry)]
    pos_x, pos_y, vel_x, vel_y = coords
    cdata.append((pos_x, pos_y, vel_x, vel_y))


def dump(seconds, xlist, ylist):
    # dump tries to compress larger star fields so they fit on the screen

    x_offset = min(xlist)
    y_offset = min(ylist)

    x_print_set = set()
    y_print_set = set()
    pos_set = set()

    for i in range(len(cdata)):
        x,y = xlist[i], ylist[i]

        x = x - x_offset
        x_print_set.add(x)
        x_print_set.add(x-1)
        x_print_set.add(x+1)

        y = y - x_offset
        y_print_set.add(y)
        y_print_set.add(y-1)
        y_print_set.add(y+1)

        pos_set.add( (x,y) )

    display = []
    for y in sorted(y_print_set):
        for x in sorted(x_print_set):
            if (x,y) in pos_set:
                display.append('X')
            else:
                display.append(' ')
        display.append('\n')

    print (''.join(display))
    print(seconds)


def get_range(xlist):
    x_min = min(xlist)
    x_max = max(xlist)
    return x_max - x_min


xlist = [i[0] for i in cdata]
ylist = [i[1] for i in cdata]
seconds = 0

while True:

    # capture before state
    before_xlist = list(xlist)
    before_ylist = list(ylist)
    before_width = get_range(xlist)
    before_height = get_range(ylist)
    before_seconds = seconds

    for i, row in enumerate(cdata):
        xlist[i] += row[2]
        ylist[i] += row[3]
    seconds += 1

    width = get_range(xlist)
    height = get_range(ylist)
    if width > before_width or height > before_height:
        break

dump(before_seconds, before_xlist, before_ylist)
