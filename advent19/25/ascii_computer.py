#!/usr/bin/env python3

import sys

import intcode

def main():

    data = intcode.load()

    sim_state = intcode.SimState('ascii', data)

    while True:
        ret = intcode.simulator(sim_state)
        if ret == "INPUT":
            buf = sys.stdin.read(1)
            if not buf:
                break
            ch = buf[0]
            b = ord(ch)
            sim_state.input.append(b)
        elif ret == "OUTPUT":
            while sim_state.output:
                b = sim_state.output.pop(0)
                if b > 0x7F:
                    print(f'\n{b}')
                else:
                    ch = chr(b)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
        elif ret == "HALT":
            break
        else:
            raise Exception(f"unknown intcode return state: {ret}")



if __name__ == "__main__":
    main()