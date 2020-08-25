#! /usr/bin/env python3

import sys
import itertools

l0 = [ 'a', 'b', 'c', 'd', 'e' ]
lists = [
    [ [1,2], [3,4], [1,3], [3,4] ],
    [ [1,2], [3,4], [5,6,7], [1,2], [6,7,8], [1,2,3] ],
    [ [1,2], [3,4], [5,6,7], [1,3], [6,7,8], [2,3], [7,8], [8,9] ],
    [ [1,2,3,4], [1,9], [1,2,3,5], [1,2,3,6], [1,3,5,6], [1,2,5,6], [1,5,6], [8,9], [1,2,3,7] ],

    [ [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8] ]
]

def spotTuple(l: list, size: int):
    print(f'Try to spot {size}-tuples on {l}')
    for cellNumbers in itertools.combinations(range(len(l)),size):
        # print(cellNumbers)
        s = set()
        cells = set()
        for cellNumber in cellNumbers:
            tupleCandidates = l[cellNumber]
            # print(f'   candidates: {tupleCandidates}')
            s.update(tupleCandidates)
            cells.add(cellNumber)
        if len(s) == size:
            print(f'**** Spotted: {s} with cells {cells}')
        else:
            # print(f'Nothing: {len(s)}')
            pass
    print('---------------------')

def main():
    # spotTuple(lists[2], 2)

    for l in lists:
        print(f'LIST {l}')
        for size in range(2,9):
            spotTuple(l, size)

if __name__ == "__main__":
    main()
