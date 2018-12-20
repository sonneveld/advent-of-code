#!/usr/bin/env python3

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
    data = f.read().strip()


# Lexer

StartT = collections.namedtuple("StartT", "")
EndT = collections.namedtuple("EndT", "")
StringT = collections.namedtuple("StringT", "value")
OpenBracketT = collections.namedtuple("OpenBracketT", "")
CloseBracketT = collections.namedtuple("CloseBracketT", "")
PipeT = collections.namedtuple("PipeT", "")

token_map = {
    "^" : StartT,
    "$" : EndT,
    "(" : OpenBracketT,
    ")" : CloseBracketT,
    "|" : PipeT
}

def tokeniser(data):
    while len(data) > 0:
        if data.startswith('|)'):
            yield PipeT()
            yield StringT('')
            yield CloseBracketT()
            data = data[2:]
            continue
        if data[0] in token_map:
            yield token_map[data[0]]()
            data = data[1:]
            continue
        m = re.match(r'^(\w+)', data)
        if m is not None:
            value = m.group(1)
            yield StringT(value)
            data = data[len(value):]
            continue
        raise Exception(f"unknown ch for tokeniser: {data[0]}")


class TokenStream(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.offset = 0

    def next(self):
        v = self.tokens[self.offset]
        # print ('next', self.offset, v)
        self.offset += 1
        return v

    def peek(self):
        v =  self.tokens[self.offset]
        # print ('peek', self.offset, v)
        return v

    def peek_type(self, token_type):
        v = self.peek()
        return isinstance(v, token_type)

    def consume(self, token_type):
        v = self.next()
        assert isinstance(v, token_type)



# Parser

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = []

def consume_branch(token_stream, prevlist):

    token_stream.consume(OpenBracketT)

    nodelist = []

    while True:
        nodelist.extend (  consume_path(token_stream, prevlist) )

        t = token_stream.next()

        if isinstance(t, CloseBracketT):
            break
        elif isinstance(t, PipeT):
            continue
        else:
            raise Exception(f"unknown token: {t}")

    return nodelist


def add_node(prevlist, n):
    for p in prevlist:
        p.next.append(n)
    return [n]

# create graph, with next links (by keeping track of prev nodes)
def consume_path(token_stream, prevlist):

    while True:

        if token_stream.peek_type(StringT):
            t = token_stream.next()
            prevlist = add_node(prevlist, Node(t.value))

        elif token_stream.peek_type(OpenBracketT):
            prevlist = consume_branch(token_stream, prevlist)
            continue

        else:
            break

    return prevlist


token_stream = TokenStream(list(tokeniser(data)))
token_stream.consume(StartT)
start_node = Node('')
consume_path(token_stream, [start_node])
token_stream.consume(EndT)


# hacky print map

def dump_map(start_node):

    room_set = set()
    south_open_set = set()
    east_open_set = set()

    seen = set()
    walkers = [(start_node, 0, 0)]

    while len(walkers) > 0:
        node, x, y = walkers.pop()

        seen_key = (id(node), x, y)
        if seen_key in seen:
            continue
        seen.add(seen_key)

        room_set.add( (x,y) )

        for ch in node.value:

            if ch == "N":
                y -= 1
                south_open_set.add( (x,y) )

            if ch == "S":
                south_open_set.add( (x,y) )
                y += 1
            if ch == "E":
                east_open_set.add( (x,y) )
                x += 1
            if ch == "W":
                x -= 1
                east_open_set.add( (x,y) )

        for n in node.next:
            walkers.append( (n, x, y) )

    x_min = min(p[0] for p in room_set)
    x_max = max(p[0] for p in room_set)
    y_min = min(p[1] for p in room_set)
    y_max = max(p[1] for p in room_set)
    print(x_min, x_max, y_min, y_max)
    for y in range(y_min, y_max+1):
        for x in range(x_min, y_max+1):
            print (" ", end="")
            if (x,y) in east_open_set:
                print(" ", end="")
            else:
                print("#", end="")
        print()
        for x in range(x_min, y_max+1):
            if (x,y) in south_open_set:
                print(" ", end="")
            else:
                print("#", end="")
            print ("#", end="")
        print()


# Process

class Room(object):
    def __init__(self):
        self.open = set()


# process and connect rooms

def connect_rooms(rooms, a, b):
    if a not in rooms:
        rooms[a] = Room()
    if b not in rooms:
        rooms[b] = Room()
    rooms[a].open.add(b)
    rooms[b].open.add(a)

rooms = {}
seen = set()
walkers = [(start_node, 0, 0)]

while len(walkers) > 0:
    node, x, y = walkers.pop()

    # collapse walker states if there's already been a walker with the same node + initial position
    seen_key = (id(node), x, y)
    if seen_key in seen:
        continue
    seen.add(seen_key)

    for ch in node.value:

        prev_room = (x,y)

        if ch == "N":
            y -= 1
        if ch == "S":
            y += 1
        if ch == "E":
            x += 1
        if ch == "W":
            x -= 1

        room = (x,y)

        connect_rooms(rooms, prev_room, room)

    for n in node.next:
        walkers.append( (n, x, y) )


# walk and get room distance information

def calc_distance(rooms):

    distance_map = {}

    work_queue = [ (0,0,0) ]

    while len(work_queue) > 0:

        x,y,distance = work_queue.pop()

        if (x,y) in distance_map:
            continue

        distance_map[ (x,y) ] = distance

        room = rooms[ (x,y) ]
        for (x,y) in room.open:
            work_queue.append( (x,y,distance+1) )

    return distance_map

distance_map = calc_distance(rooms)



# Part 1

print (max([x for x in distance_map.values()]))

# Part 2

print (len([x for x in distance_map.values() if x >= 1000]))
