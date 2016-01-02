#!/usr/bin/env python

s = open('day8.in').read()

print sum(len(x) - len(eval(x)) for x in s.split())

d = { "\\" : 2, r'"': 2 }
def r(s):
    return sum(d.get(x, 1) for x in s) + 2

print sum(r(x) - len(x) for x in s.split())
