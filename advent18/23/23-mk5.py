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

with open(input_filename) as f:
    for line in f:
        x,y,z,r = [int(x) for x in re.findall(r'[\-\+]?[\d]+', line)]
        data.append( (x,y,z,r) )



def calc_manhattan_distance(x1,y1,z1, x2,y2,z2):
    return abs(x1-x2) + abs(y1-y2) + abs (z1-z2)


# print (data)

bot_with_largest_radius = max( (b for b in data), key=lambda b: b[3] )

# print (data.index(bot_with_largest_radius))

count = 0
for b in data:
    md = calc_manhattan_distance(b[0], b[1], b[2], bot_with_largest_radius[0],bot_with_largest_radius[1], bot_with_largest_radius[2])
    if md <= bot_with_largest_radius[3]:
        count += 1

# print(count)

# print('part 2')

def min_max(seq):
    seq = list(seq)
    result =  min(seq), max(seq)
    print (result)
    return result



# def sphere_coords(sx,sy,sz,r):
#     x_min, x_max = sx - r - 1, sx+r+1
#     y_min, y_max = sy - r - 1 , sy + r + 1
#     z_min, z_max = sz - r - 1 , sz + r + 1

#     for x in range(x_min, x_max+1):
#         for y in range(y_min, y_max+1):
#             for z in range(z_min, z_max+1):
#                 md = calc_manhattan_distance(sx,sy, sz, x, y, z)
#                 if md <= r:
#                     yield (x,y,z)


def spheres_collide(s1, s2):
    distance = calc_manhattan_distance(s1[0], s1[1], s1[2], s2[0], s2[1], s2[2])
    return  s1[3]+s2[3] >= distance


search_space = []

for b in data:
    search_space.append( (b[0], b[1], b[2], 0 ))


result = []

best_value = None


data_scored = []






# print (data.index(bot_with_largest_radius))

# count = 0
# for b in data:
#     md = calc_manhattan_distance(b[0], b[1], b[2], bot_with_largest_radius[0],bot_with_largest_radius[1], bot_with_largest_radius[2])
#     if md <= bot_with_largest_radius[3]:
#         count += 1



# while len(search_space) > 0:

#     e = search_space.pop(0)


#     s = sum(1 for b in data if spheres_collide(e, b))
#     result.append( (s, b[0], b[1], b[2])  )

#     md = calc_manhattan_distance(b[0], b[1], b[2], 0,0,0)

#     if best_value is None or best_value < (s, md):
#         best_value = (s, md)


print (best_value)

x_min = min(b[0]-b[3] for b in data)
x_max = max(b[0]+b[3] for b in data)

y_min = min(b[1]-b[3] for b in data)
y_max = max(b[1]+b[3] for b in data)

z_min = min(b[2]-b[3] for b in data)
z_max = max(b[2]+b[3] for b in data)


r_min = min(b[3] for b in data)
r_max = max(b[3] for b in data)


print (x_min, y_min, z_min, "---", x_max, y_max, z_max)
print(r_min, r_max)


random.seed(None)

best = None
seen = set()


def num_in_range(x,y,z):

    return sum(1 for bx,by,bz,br in data if calc_manhattan_distance(x,y,z, bx, by, bz) <= br)

    # count = 0
    # for bx,by,bz,br in data:
    #     md = calc_manhattan_distance(x,y,z, bx, by, bz)
    #     if md <= br:
    #         count += 1
    # return count

scored_data= []
for entry in data:

    count = 0
    for other in data:
        if spheres_collide(entry, other):
            count += 1

    scored_data.append( (count, entry[0], entry[1], entry[2], entry[3]) )

scored_data.sort()
# print (scored_data)

# for count in range(100):


SELECTION_SIZE = 4000


selection = []

for b in data:
    selection.append( (None, b[0], b[1], b[2]) )

selection.append( (None, 0,0,0) )


# extra =  [(866, 15216285, 60247328, 29093400), (856, 17676858, 62343674, 27152681), (855, 20056098, 61786567, 30069832), (854, 17271194, 61368962, 30849745), (853, 19992067, 61012433, 29472395)]
# selection.extend(extra)

# extra = [(870, 16990905, 61059405, 27783082), (866, 15216285, 60247328, 29093400), (856, 17676858, 62343674, 27152681), (855, 20056098, 61786567, 30069832), (854, 17271194, 61368962, 30849745)]
# selection.extend(extra)
# extra = [(872, 17218504, 59435194, 28823499), (870, 16990905, 61059405, 27783082), (866, 15216285, 60247328, 29093400), (864, 16146370, 60396499, 29688250), (862, 17631226, 61361799, 26917543)]
# selection.extend(extra)
# extra = [(872, 17219471, 59435244, 28823627), (872, 17219464, 59435369, 28823648), (872, 17219436, 59435351, 28823627), (872, 17219434, 59435279, 28823668), (872, 17219429, 59435344, 28823551)]
# selection.extend(extra)

# extra = [(875, 16097699, 59435244, 28823627), (875, 16097699, 59435244, 28823627), (875, 16097699, 59435244, 28823627), (875, 16097699, 59435244, 28823627), (875, 16097699, 59435244, 28823627)]
# selection.extend(extra)

# extra = [(893, 15205686, 59435244, 28823627)]
extra = [(902, 15192122, 59425490, 28800353), (902, 15193231, 59426547, 28802519), (902, 15203541, 59436014, 28822296), (902, 15205648, 59435164, 28823553), (902, 15205644, 59435321, 28823706), (900, 15205756, 59435218, 28823714), (900, 15205672, 59435180, 28823591), (900, 15205656, 59435294, 28823690)]
extra = [(903, 15108103, 59330118, 28620962), (902, 15117040, 59341563, 28641344)]
selection.extend(extra)



best_score = 0

scored_data = [x for x in scored_data if x[0] >= best_score]

while len(selection) < SELECTION_SIZE:
    bs,x,y,z,r = random.choice(scored_data)
    x = random.randint(x-r, x+r)
    y = random.randint(y-r, y+r)
    z = random.randint(z-r, z+r)
    selection.append ( (None, x,y,z) )


cur = (14704575, 58920257, 27807573)

while True:

    cur_score = num_in_range(cur[0], cur[1], cur[2])
    cur_mh = calc_manhattan_distance(0,0,0, cur[0], cur[1], cur[2])

    print (cur_mh, cur_score, cur)

    for xv in range(-10, 10):
        for yv in range(-10, 10):
            for zv in range(-10, 10):
                x = cur[0] + xv
                y = cur[1] + yv
                z = cur[2] + zv
                next_score =  num_in_range(x,y,z)
                next_mh = calc_manhattan_distance(0,0,0, x,y,z)
                if next_score > cur_score:
                    cur = (x,y,z)

                elif next_score == cur_score and next_mh < cur_mh:
                    cur = (x,y,z)
