#! /usr/bin/env python3

import sys
from solver import Solver
from cell import Cell

def main():
    solver = Solver(sys.argv[1])
    solver.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()