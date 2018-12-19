#!/usr/bin/env python3

'''
Environment variables supported:
DEBUG=  - enable debugging
REG0=<int>  - override initial reg0 value (for part 2)
'''

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



def do_instruction(reg, instruction):
    reg = list(reg)
    opname, a,b,c = instruction
    if opname == "addr":
        reg[c] = reg[a] + reg[b]
    elif opname == 'addi':
        reg[c] = reg[a] + b
    elif opname == 'mulr':
        reg[c] = reg[a] * reg[b]
    elif opname == 'muli':
        reg[c] = reg[a] * b
    elif opname == 'banr':
        reg[c] = reg[a] & reg[b]
    elif opname == 'bani':
        reg[c] = reg[a] & b
    elif opname == 'borr':
        reg[c] = reg[a] | reg[b]
    elif opname == 'bori':
        reg[c] = reg[a] | b
    elif opname == 'setr':
        reg[c] = reg[a]
    elif opname == 'seti':
        reg[c] = a
    elif opname == 'gtir':
        reg[c] = 1 if a > reg[b] else 0
    elif opname == 'gtri':
        reg[c] = 1 if reg[a] > b else 0
    elif opname == 'gtrr':
        reg[c] = 1 if reg[a] > reg[b] else 0
    elif opname == 'eqir':
        reg[c] = 1 if a == reg[b] else 0
    elif opname == 'eqri':
        reg[c] = 1 if reg[a] == b else 0
    elif opname == 'eqrr':
        reg[c] = 1 if reg[a] == reg[b] else 0
    else:
        raise Exception(f"unknown name {op_name}")
    return reg



ip_reg = None
for line in data:
    if line[0] == "#":
        ip_reg = int(line[-1])

code = []
for line in data:
    if line[0] == "#":
        continue
    tokens = line.split()
    instruction = tokens[:1] + [int(x) for x in tokens[1:]]
    code.append(instruction)

ip = 0
regs = [0] * 6

regs[0] = 0
if "REG0" in os.environ:
    regs[0] = int(os.environ["REG0"])

instruction_count = 0

while ip >= 0 and ip < len(code):

    c = code[ip]
    regs[ip_reg] = ip

    if DEBUG:
        debug = f"ip={ip} {regs} {' '.join(str(x) for x in c)}"
        print (debug, end="")

    regs = do_instruction(regs, c)
    instruction_count += 1

    if DEBUG:
        debug = f" {regs}"
        print(debug)

    ip = regs[ip_reg]
    ip += 1

print("HALT")
print("instruction count:", instruction_count)
print("r0 =",regs[0])
