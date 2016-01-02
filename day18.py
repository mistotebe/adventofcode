#!/usr/bin/env python

def step(s, stuck=[]):
    n = [[False]*size for x in r]
    for x in r:
        for y in r:
            c = sum(int(s[a][b]) for a in range(x-1, x+2) if a >= 0 and a < size for b in range(y-1, y+2) if b >= 0 and b < size and (x,y) != (a,b))
            if s[x][y] and c in (2,3):
                n[x][y] = True
            elif not s[x][y] and c == 3:
                n[x][y] = True
            else:
                n[x][y] = ((x,y) in stuck)
    return n

steps, s = 5, """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

steps, s = 100, open('day18.in').read()

def show(s):
    return '\n'.join(["".join([c and '#' or '.' for c in l]) for l in s])

d1 = [[c == '#' for c in l] for l in s.split() if l]
d2 = [list(l) for l in d1]

size = len(d1)
r = range(size)
stuck = [(0,0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]

for x,y in stuck:
    d2[x][y] = True

for x in range(steps):
    d1 = step(d1)
    d2 = step(d2, stuck)

print sum(sum(int(x) for x in l) for l in d1)
print sum(sum(int(x) for x in l) for l in d2)
