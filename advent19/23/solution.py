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


from intcode import load, SimState, simulator


# ----------------------------------------------------------------------------------------------------------------------
# SOLUTION
# ----------------------------------------------------------------------------------------------------------------------

class Computer:

    def __init__(self, data, address):
        self.address = address
        self.sim_state = SimState('func', data)
        self.sim_state.input.append(address)
        self.queue = []
        self.idle = False


    def process(self):

        self.idle = True

        ret = simulator(self.sim_state)

        if ret == "INPUT":

            if self.queue:
                p = self.queue.pop(0)
                x,y = p
                assert x is not None
                print(f'[{self.address}]\tProcessing packet {x} {y}')
                self.sim_state.input.append(x)
                self.sim_state.input.append(y)
                self.idle = False
            else:
                # print(f'[{self.address}]\tQueue empty')
                self.sim_state.input.append(-1)

        elif ret == "OUTPUT":

            self.idle = False

            # read the next two numbers of the packet!
            ret = simulator(self.sim_state)
            assert(ret == 'OUTPUT')
            ret = simulator(self.sim_state)
            assert(ret == 'OUTPUT')

            assert len(self.sim_state.output) == 3

            packet = []
            packet.append(self.sim_state.output.pop(0))
            packet.append(self.sim_state.output.pop(0))
            packet.append(self.sim_state.output.pop(0))

            print(f'[{self.address}]\tGenerated packet {packet}')

            return packet

        else:
            raise Exception(f'Unexpected: {ret}')

        return None

    def send_packet(self, x, y):
        self.queue.append ((x, y))
        print(f'[{self.address}]\tQueued packet: {x} {y} : Queue size:{len(self.queue)}')



def simulate_network(data):

    computers = []
    for x in range(50):
        computers.append( Computer(data, x) )

    iteration = 0
    packet_count = 0

    nat_x,nat_y = None, None
    idle_count = 10
    nat_sent_list = []

    msg_queue = []

    while True:
        print()
        print(f"---- Iteration {iteration} ----")
        print(f'[SYS]\tpacket count: {packet_count}  switch queue: {len(msg_queue)}')
        print()
        iteration += 1

        for c in computers:

            c_idle_count = 10
            while c_idle_count > 0:
                p = c.process()
                if p is not None:

                    if p[0] == 255:
                        print("[NAT]\tStoring:", p[1], p[2])
                        nat_x, nat_y = p[1], p[2]
                    else:
                        msg_queue.append(p)

                if not c.idle:
                    c_idle_count = 10
                c_idle_count -= 1


        if msg_queue:
            print()

        while msg_queue:
            address,x,y = msg_queue.pop(0)

            print('[SYS]\tForwarding:', address, x, y)
            computers[address].send_packet(x,y)
            packet_count += 1


        is_idle = all(c.idle and len(c.queue) <= 0 for c in computers)

        if is_idle:
            print()
            print("[SYS]\tIdle detected")
            if nat_x is not None:
                print('[NAT]\tNotifying:', 0, nat_x, nat_y)
                nat_sent_list.append(nat_y)
                if  len(nat_sent_list) > 2 and nat_sent_list[-1] == nat_sent_list[-2]:
                    # DONE!
                    break
                computers[0].send_packet(nat_x,nat_y)
                packet_count += 1


    print()
    print(nat_sent_list[0])
    print(nat_sent_list[-1])

def main():
    data = load()
    simulate_network(data)


if __name__ == "__main__":
    main()
