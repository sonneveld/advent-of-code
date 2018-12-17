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
    data.sort()


guard_id = None
sleep_start = None
sleep_end = None

minute_data = []
guard_sleeps = collections.Counter()

for entry in data:

    m = re.search(r'(\d+):(\d+)', entry)
    hour, minute = [int(x) for x in m.group(1, 2)]

    m = re.search(r'Guard #(\d+) begins shift', entry)
    if m is not None:
        guard_id = int(m.group(1))
        sleep_start = None
        sleep_end = None

    if 'falls asleep' in entry:
        sleep_start = minute
        sleep_end = None

    if 'wakes up' in entry:
        sleep_end = minute
        for x in range(sleep_start, sleep_end):
            minute_data.append( (guard_id, x) )
        guard_sleeps[guard_id] += (sleep_end - sleep_start)
        sleep_start = None
        sleep_end = None


# Part 1

sleepiest_guard_id = guard_sleeps.most_common(1)[0][0]

minute_sleeps = collections.Counter( t for (id,t) in minute_data if id == sleepiest_guard_id  )
print(minute_sleeps.most_common(1)[0][0]  * sleepiest_guard_id)


# Part 2

guard_id = -1
longest_minute = -1
num_sleeps = -1

for minute in range(60):

    guard_ids = [x[0] for x in minute_data if x[1] == minute]
    guard_counter = collections.Counter(guard_ids)
    most_common = guard_counter.most_common(1)
    if len(most_common) > 0:
        most_common = most_common[0]
        if most_common[1] > num_sleeps:
            guard_id = most_common[0]
            num_sleeps = most_common[1]
            longest_minute = minute

print (guard_id * longest_minute)
