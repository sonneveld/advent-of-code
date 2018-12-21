#!/usr/bin/env python3

seen = set()
first_halting = None
last_halting = None

with open('halting_values.txt') as f:

        for line in f:
                x = int(line)
                if first_halting is None:
                        first_halting = x
                if x in seen:
                        break
                last_halting = x
                seen.add(x)

print (first_halting)
print (last_halting)
