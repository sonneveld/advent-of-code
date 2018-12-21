#!/usr/bin/env python3

data = open('halting_values.txt').readlines()
data = [int(x) for x in data]
seen = set()
first_halting = data[0]
last_halting = None
for x in data:
        if x in seen:
                break
        last_halting = x
        seen.add(x)

print (first_halting)
print (last_halting)
