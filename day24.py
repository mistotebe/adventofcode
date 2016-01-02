#!/usr/bin/env python3

from operator import mul
from functools import partial

q = lambda x: (min(map(len, x)), min(map(partial(reduce, mul), x)), x)
qe = lambda x: min(map(q, x))

def reduce(f, x):
    r, *rest = x
    while rest:
        c, *rest = rest
        r = f(r, c)
    return r

def dist(l, limit=0, buckets=3, s=None, rest=None):
    rest = rest or []
    s = s or [[] for i in range(buckets)]
    sums = [sum(x) for x in s]
    c = int(sums[0] == limit)
    if len(s[0]) >= 7:
        return
    for i in range(len(l)):
        if sums[c] + l[i] > limit:
            break
        #print(l, s, rest, sums, c, i)
        l_copy = l[i+1:]
        s_copy = [x[:] for x in s]
        rest_copy = rest + l[:i]

        s_copy[c].append(l[i])
        if sums[c] + l[i] == limit:
            l_copy = rest_copy + l_copy
            rest_copy = []
            if c == buckets - 2:
                s_copy[-1] = l_copy
                if s_copy[0] < s_copy[1] < s_copy[2]:
                    yield s_copy
                return

        yield from dist(l_copy, limit=limit, s=s_copy, rest=rest_copy)

d = sorted(map(int, open('day24.in').read().split()))
#d = sorted(x for x in range(12) if x % 6)
buckets = 3
limit = sum(d) // buckets

for x in dist(d, limit):
    print(qe([x]))
    break

buckets = 4
limit = sum(d) // buckets

for x in dist(d, limit):
    print(qe([x]))
    break
