#!/usr/bin/env python

d = [[22, 8, 165], [8, 17, 114], [18, 6, 103], [25, 6, 145], [11, 12, 125], [21, 6, 121], [18, 3, 50], [20, 4, 75], [7, 20, 119]]

def travelled(v, e, r, t):
    d = v * e
    c = e + r
    n, l = t // c, t % c
    if l >= e:
        n += 1
        l = 0
    return n*d + l*v

print max(travelled(v, e, r, 2503) for (v, e, r) in d)

dists = [max(travelled(v, e, r, t) for (v, e, r) in d) for t in xrange(2503+1)]
print max(len([t for t in xrange(1, 2503+1) if travelled(v, e, r, t) == dists[t]]) for (v, e, r) in d)
