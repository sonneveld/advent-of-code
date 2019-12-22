#!/usr/bin/env python3

import sys
import os
import os.path
import re

import collections
import functools
import heapq
import itertools
import math
import multiprocessing
import random
import string
import time

from collections import Counter
from collections import defaultdict
# from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from itertools import product
from multiprocessing import Pool

import lcg_crack
from lcgrandom import LcgRandom

DEBUG=False

def load():
    filename = "input"
    if len(sys.argv) >= 2:
        filename = sys.argv[1]

    result = []
    with open(filename) as f:
        data = f.readlines()
        data = [x.strip() for x in data]
        for line in data:
            tokens = line.split()
            if line.startswith('cut'):
                result.append( ('cut', int(tokens[-1])))
            elif line.startswith('deal with increment'):
                result.append(('deal-increment', int(tokens[-1])))
            elif line.startswith('deal into new stack'):
                result.append(('deal-new', None))


        return result

# -------------------------------------------------------------------------------------------------------------------
# PART ONE
# -------------------------------------------------------------------------------------------------------------------

def shuffle_deck(data, deck):

    def reverse_deck(old_stack):
        old_stack.reverse()
        return old_stack

    def rotate_deck(stack, n):
        d = collections.deque(stack)
        d.rotate(-n)
        return list(d)

    def mul_mod_deck(stack, n):
        new_stack = [None] * len(stack)
        for i in range(len(stack)):
            other_i = (i*n)%len(stack)
            new_stack[other_i] = stack[i]
        return new_stack

    for cmd, n in data:
        if cmd == 'cut':
            deck = rotate_deck(deck, n)
        elif cmd == "deal-increment":
            deck = mul_mod_deck(deck, n)
        elif cmd == "deal-new":
            deck = reverse_deck(deck)

    return deck



def unshuffle_deck(data, deck):

    def reverse_deck(old_stack):
        old_stack.reverse()
        return old_stack

    def rotate_deck(stack, n):
        d = collections.deque(stack)
        d.rotate(n)
        return list(d)

    def mul_mod_deck(stack, n):
        new_stack = [None] * len(stack)
        for i in range(len(stack)):
            other_i = (i*n)%len(stack)
            new_stack[i] = stack[other_i]
        return new_stack

    for cmd, n in reversed(data):
        if cmd == 'cut':
            deck = rotate_deck(deck, n)
        elif cmd == "deal-increment":
            deck = mul_mod_deck(deck, n)
        elif cmd == "deal-new":
            deck = reverse_deck(deck)

    return deck


def part_1(data):
    NUM_CARDS = 10007
    deck = list(range(NUM_CARDS))
    deck = shuffle_deck(data, deck)
    return deck.index(2019)


# -------------------------------------------------------------------------------------------------------------------
# PART TWO
# -------------------------------------------------------------------------------------------------------------------

def shuffle_card_in_deck(data, deck_size, card_index):

    # positive is left
    def rotate_deck(deck_size, card_index, n):
        i = (card_index - n) % deck_size
        return i

    def mul_mod_deck(deck_size, card_index, n):
        i = (card_index * n) % deck_size
        return i

    def reverse_deck(deck_size, card_index):
        i = deck_size - card_index - 1
        return i

    for cmd, n in data:
        if cmd == 'cut':
            card_index = rotate_deck(deck_size, card_index, n)
        elif cmd == "deal-increment":
            card_index = mul_mod_deck(deck_size, card_index, n)
        elif cmd == "deal-new":
            card_index = reverse_deck(deck_size, card_index)

    return card_index


def unshuffle_card_in_deck(data, deck_size, card_index):

    # positive is left
    def rotate_deck(deck_size, card_index, n):
        i = (card_index + n) % deck_size
        return i

    def mul_mod_deck(deck_size, card_index, n):
        for fudge in range(0, n):
            (q,r) = divmod(fudge*deck_size + card_index, n)
            if r == 0:
                return q

        raise Exception("uh oh")


    def reverse_deck(deck_size, card_index):
        i = deck_size - card_index - 1
        return i

    for cmd, n in reversed(data):
        if cmd == 'cut':
            card_index = rotate_deck(deck_size, card_index, n)
        elif cmd == "deal-increment":
            card_index = mul_mod_deck(deck_size, card_index, n)
        elif cmd == "deal-new":
            card_index = reverse_deck(deck_size, card_index)

    return card_index

def part_2(data):
    '''
    Shuffling a single card produces an LCG pseudorandom sequence.
    1) "Unshuffle" cards backwards (doesn't matter where from), determine first few items in sequence
    2) Determine modulus, multiplier, increment. (We know modulus from number of cards)
    3) Skip through LCG sequence to get final number.
    '''
    
    NUM_CARDS = 119315717514047
    NUM_SHUFFLES = 101741582076661
    seed = 2020

    # generate some numbers so we can figure out state
    card_index = 0
    states = []
    for x in range(10):
        states.append(card_index)
        card_index = unshuffle_card_in_deck(data, NUM_CARDS, card_index)

    # the known modulus is NUM_CARDS, since that is the period it repeats
    modulus, multiplier, increment = lcg_crack.crack_unknown_multiplier(states, NUM_CARDS)

    # skip ahead
    randfast = LcgRandom(multiplier, increment, modulus, seed)
    randfast.skip(NUM_SHUFFLES)
    return randfast.get_state()


def part_2_alternative(data):
    '''
    Alternative version that uses sequence from shuffling forwards
    
    Shuffling a single card produces an LCG pseudorandom sequence.
    1) Shuffle cards forwards a few times to determine first few items in sequence
    2) Determine modulus, multiplier, increment. (We know modulus from number of cards)
    3) Skip through LCG sequence to get final number.

    We know cards repeat every NUM_CARDS shuffles, so we can skip ahead NUM_CARDS - NUM_SHUFFLES
    Alternatively, we can skip -NUM_SHUFFLES cause the lib allows it. :)
    '''
    
    NUM_CARDS = 119315717514047
    NUM_SHUFFLES = 101741582076661
    seed = 2020

    # generate some numbers so we can figure out state
    card_index = 0
    states = []
    for x in range(10):
        states.append(card_index)
        card_index = shuffle_card_in_deck(data, NUM_CARDS, card_index)

    # the known modulus is NUM_CARDS, since that is the period it repeats
    modulus, multiplier, increment = lcg_crack.crack_unknown_multiplier(states, NUM_CARDS)

    # skip ahead
    randfast = LcgRandom(multiplier, increment, modulus, seed)
    if True:
        randfast.skip(NUM_CARDS - NUM_SHUFFLES - 1)
    else:
        randfast.skip(-NUM_SHUFFLES)
    return randfast.get_state()


def main():
    data = load()
    v = part_1(data)
    print(v)
    v = part_2(data)
    print(v)


if __name__ == "__main__":
    main()
