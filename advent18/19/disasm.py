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
    data = [x.strip() for x in f.readlines()]



def disasm(instruction):
    opname, a,b,c = instruction
    if opname == "addr":
        return f"r{c} = r{a} + r{b}"
    elif opname == 'addi':
        return f"r{c} = r{a} + {b}"
    elif opname == 'mulr':
        return f"r{c} = r{a} * r{b}"
    elif opname == 'muli':
        return f"r{c} = r{a} * {b}"
    elif opname == 'banr':
        return f"r{c} = r{a} & r{b}"
    elif opname == 'bani':
        return f"r{c} = r{a} & {b}"
    elif opname == 'borr':
        return f"r{c} = r{a} | r{b}"
    elif opname == 'bori':
        return f"r{c} = r{a} | {b}"
    elif opname == 'setr':
        return f"r{c} = r{a}"
    elif opname == 'seti':
        return f"r{c} = {a}"
    elif opname == 'gtir':
        return f"r{c} = {a} > r{b}"
    elif opname == 'gtri':
        return f"r{c} = r{a} > {b}"
    elif opname == 'gtrr':
        return f"r{c} = r{a} > r{b}"
    elif opname == 'eqir':
        return f"r{c} = {a} == r{b}"
    elif opname == 'eqri':
        return f"r{c} = r{a} == {b}"
    elif opname == 'eqrr':
        return f"r{c} = r{a} == r{b}"
    else:
        raise Exception(f"unknown instruction {instruction}")


def peephole(ip, ip_reg, asm):

    asm = asm.replace(f"r{ip_reg}", "ip")

    if "ip = " not in asm:
        asm = asm.replace("ip", f"{ip}")

    m = re.match(r'ip = ip \+ (\d+)', asm)
    if m is not None:
        to = int(m.group(1))
        asm = f'goto {ip+to+1:04}'

    m = re.match(r'ip = (\d+)', asm)
    if m is not None:
        to = int(m.group(1))
        asm = f'goto {to+1:04}'

    if asm == "ip = ip * ip":
        asm = "halt"

    condition = None
    m = re.match(r'ip = ip \+ (r\d+)', asm)
    if m:
        condition = m.group(1)
    m = re.match(r'ip = (r\d+) \+ ip', asm)
    if m:
        condition = m.group(1)

    if condition is not None:
        asm = f"if ({condition}) goto {ip+2:04}"

    return asm


# separate basic blocks
def find_breaks(ip, asm):
    result = set()
    if 'goto' in asm:
        result.add(ip)
        n = int(asm.split()[-1])
        result.add(n-1)
    if 'halt' in asm:
        result.add(ip)
    return result



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

result = []
breaks = set()
for ip, instruction in enumerate(code):
    asm = disasm(instruction)
    asm = peephole(ip, ip_reg, asm)
    breaks |= find_breaks(ip, asm)
    result.append(asm)

for ip, asm in enumerate(result):
    print (f"{ip:04} {asm}")
    if ip in breaks:
        print()
