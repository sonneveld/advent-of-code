
import sys
import os
import os.path
import re
from collections import Counter

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    with open(filename) as f:
        data = f.readline()
        data = data.split("-")
        data = [int(x) for x in data]
        return data


def part_1(first, last):
        
    for x in range(first, last+1):

        digits = list(str(x))
        digits_sorted = list(sorted(digits))

        if digits != digits_sorted:
            continue
            
        okay = False
        counted = Counter(digits)

        for digit in digits:
            if counted[digit] >= 2: 
                okay = True

        if okay:
            yield x

def part_2(first, last):

    for x in range(first, last+1):

        digits = list(str(x))
        digits_sorted = list(sorted(digits))

        if digits != digits_sorted:
            continue

        okay = False
        counted = Counter(digits)

        for digit in digits:
            if counted[digit] == 2: 
                okay = True

        if okay:
            yield x


def main():

    first, last = load()

    result = len(list(part_1(first, last)))
    print(result)

    result = len(list(part_2(first, last)))
    print(result)


if __name__ == "__main__":
    main()
