import re
import collections

import sys

try:
    input_filename = sys.argv[1]
except IndexError:
    input_filename = "input.txt"

with open(input_filename) as f:
    data = f.read()

data = data.split("\n\n\n\n")
data = data[0]
data = data.split("\n\n")

op_names = """addr
addi
mulr
muli
banr
bani
borr
bori
setr
seti
gtir
gtri
gtrr
eqir
eqri
eqrr""".split('\n')


def do_instruction(opname, instruction, reg):
    orig = list(reg)
    reg = list(reg)
    a,b,c = instruction[1:]
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
    # print (opname, a, b, c, "|", orig, "->", reg, 'result', reg[c])
    return reg


op_possibles = [None]*16
for x in range(16):
    op_possibles[x] = set(op_names)


count = 0

for entry in data:
    lines = entry.split("\n")
    before = [int(x) for x in re.findall(r'\d+', lines[0])]
    instruction = [int(x) for x in re.findall(r'\d+', lines[1])]
    after = [int(x) for x in re.findall(r'\d+', lines[2])]

    op = instruction[0]

    possibles = set()

    for op_name in op_names:
        reg = list(before)
        reg = do_instruction(op_name, instruction, reg)
        if reg == after:
            possibles.add(op_name)

    assert len(possibles) > 0

    if len(possibles) >= 3:
        count += 1

    op_possibles[op] = op_possibles[op].intersection( possibles)

multi = [x for x in op_possibles if len(x) >= 3]
print(len(multi))



# Part 2

with open(input_filename) as f:
    data = f.read()

data = data.split("\n\n\n\n")
data = data[1]
data = data.splitlines()
data = [ [int(x) for x in line.split()] for line in data   ]


# I was going to iterate permutations before I realisd you could use deduction
# def generate_permutations(op_possibles):
#     result = []
#     def try_with(op_name, cur):
#         cur = list(cur)
#         cur.append(op_name)
#         index = len(cur)
#         if len(cur) == 16:
#             result.append(cur)
#         if index >= len(op_possibles):
#             return
#         next_names = op_possibles[index] - set(cur)
#         for name in next_names:
#             try_with(name, cur)
#     cur = []
#     for x in op_possibles[0]:
#         try_with(x, cur)
#     return result


# reduce possible names
while True:
    singulars = [list(x)[0] for x in op_possibles if len(x) == 1]

    new_possibles = []
    for i, pos in enumerate(op_possibles):
        if len(pos) == 1:
            new_possibles.append(pos)
        else:
            new_possibles.append( [x for x in pos if x not in singulars] )

        op_possibles = new_possibles

    if len(singulars) == len(op_possibles):
        break

op_name_map = [list(x)[0] for x in op_possibles]

regs = [0] * 4
for instruction in data:
    op = instruction[0]
    op_name = op_name_map[op]
    regs = do_instruction(op_name, instruction, regs)

print(regs[0])
