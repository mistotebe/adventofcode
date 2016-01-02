#!/usr/bin/env python

d = [47, 46, 36, 36, 32, 32, 31, 30, 28, 26, 19, 15, 11, 11, 5, 3, 3, 3, 1, 1]

def opts(s, t, u=0, c=-1):
    if not s:
        return 0
    x, r = s[0], s[1:]
    a = opts(r, t, u, c)
    if x + u > t or c == 0:
        return a
    elif x + u == t:
        return 1 + a
    else:
        return opts(r, t, u+x, c-1) + a

print opts(d, 150)

print opts(d, 150, 0, 4)
