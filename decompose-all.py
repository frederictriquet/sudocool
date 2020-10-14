#! /usr/bin/env python3

import sys
import itertools

# decompose.py total [ [-] suite de chiffres ]
# decompose le total en utilisant nb chiffres parmi la suite
# par defaut :
# - suite de chiffres = 1..9
# - si on precise le "-", alors c'est 1..9 moins la suite de chiffres

def outies(nbs, selectednbs):
    return sorted(list(set(nbs) - set(selectednbs)))

def main():
    total = int(sys.argv[1])
    if len(sys.argv) > 2:
        if sys.argv[2] == '-':
            notNb = set([ int(x) for x in sys.argv[3:] ])
            allNb = set([ x for x in range(1,10) ])
            nb = list(allNb - notNb)
    else:
        nb = [ x for x in range(1,10) ]
    print(f'With {nb}')
    for howMany in range(1,10):
        combinations = itertools.combinations(nb, howMany)
        for c in combinations:
            if sum(c) == total:
                print(c, '   ', outies(nb, c))

if __name__ == "__main__":
    # execute only if run as a script
    main()