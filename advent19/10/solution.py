#!/usr/bin/env python3

import sys
import os
import os.path
import re
import itertools
from collections import Counter
import math

DEBUG=False

'''
def chunker(l, n):
    chunk = []
    for x in l:
        chunk.append(x)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        assert(len(chunk) == n)
        yield chunk
'''


def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    data = []
    with open(filename) as f:
        for line in f:
            data.append(re.findall(r'#|\.', line))
    return data



def get_distance(p1, p2):
    return math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2  )

def is_on_line(p1, p2, c):
    a = get_distance(p1, c) + get_distance(p2, c)
    b = get_distance(p1, p2)
    return abs(a-b) < 1


def are_points_on_line(p1, p2, points):

    for p in points:
        if is_on_line(p1, p2, p):
            return True
    return False

def part_1(data):

    asteroids = set()
    points = set()

    for y, row in enumerate(data):
        for x, it in enumerate(row):
            points.add( (x, y) )
            if it == '#':
                asteroids.add( (x, y) )

    results = []

    for asteroid in asteroids:

        others = set(asteroids)
        others.remove(asteroid)

        vectors = set()

        for other in others:
            d = get_distance(asteroid, other)
            v = ((other[0] - asteroid[0])/d, (other[1] - asteroid[1])/d)
            v = f'%0.10f,%0.10f'%(v[0], v[1])
            vectors.add(v)

        results.append( (len(vectors), asteroid) )

    return max(results)



# --------------------------------------------------------------------------------------------------------------------
# PART TWO
# --------------------------------------------------------------------------------------------------------------------

def find_angle(p1, p2):
    dp = p1[0]*p2[0] + p1[1]*p2[1]
    return math.acos(dp)

def vector_angle(v):

    if v[0] >= 0 and v[1] <= 0:
        # right up
        a = find_angle( (0.0, -1.0), v) * 180 / math.pi

    elif v[0] >= 0 and v[1] >= 0:
        # rightdown
        a = find_angle( (1.0, 0.0), v) * 180 / math.pi  + 90.0

    elif v[0] <= 0 and v[1] >= 0:
        # left down
        a = find_angle( (0.0, 1.0), v) * 180 / math.pi  + 90.0 + 90.0

    elif v[0] <= 0 and v[1] <= 0:
        a = find_angle( (-1.0, 0.0), v) * 180 / math.pi  + 90.0 + 90.0 + 90.0
        # left up

    else:
        raise Exception(f'dunno: {v}')

    return a

def part_2(data, start_pos):

    asteroids = set()
    points = set()

    for y, row in enumerate(data):
        for x, it in enumerate(row):
            points.add( (x, y) )
            if it == '#':
                asteroids.add( (x, y) )

    asteroid = start_pos

    others = set(asteroids)
    others.remove(asteroid)

    vectors = list()

    north = (0.0, -1.0)

    angles = set()

    for other in others:
        d = get_distance(asteroid, other)
        v = ((other[0] - asteroid[0])/d, (other[1] - asteroid[1])/d)
        v_id = (int(v[0]*1000000), int(v[1]*1000000))

        angle = int(vector_angle(v) * 1000)

        vectors.append( [angle, d, other] )

    vectors.sort()


    i = 1
    seen = set()
    last_angle = None
    while True:
        for angle, d, other in vectors:
            if angle == last_angle: continue
            last_angle = angle
            if other in seen:
                continue

            print(f'The {i}th asteroid to be vaporized is at {other}.')

            if i == 200:
                return other
                
            i += 1
            seen.add(other)
        else:
            break



def main():
    data = load()

    vlen, pos = part_1(data)
    print(vlen)

    v = part_2(data, pos)
    print(v[0]*100 + v[1])


if __name__ == "__main__":
    main()
