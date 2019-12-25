all_items = """monolith
astronaut ice cream
hologram
ornament
asterisk
fixed point
dark matter
antenna
""".splitlines()

import functools
import itertools

# clean slate
for item in all_items:
    print(f'drop {item}')

for comb_length in range(1, len(all_items)+1):

    for comb_items in itertools.combinations(all_items, comb_length):
        print()

        for item in comb_items:
            print(f'take {item}')
        print("east") 
        # game will quit when correct items picked up
        for item in comb_items:
            print(f'drop {item}')
        print()