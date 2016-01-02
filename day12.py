#!/usr/bin/env python

import json

f = lambda x: True

def s(j):
    if not f(j):
        return 0
    if isinstance(j, (int, long)):
        return j
    if isinstance(j, basestring):
        return 0
    if isinstance(j, dict):
        return sum(s(k) + s(v) for k,v in j.iteritems())
    if hasattr(j, '__iter__'):
        return sum(map(s, j))
    raise ValueError, j

data = json.load(open('day12.in'))

print s(data)

f = lambda x: not (isinstance(x, dict) and 'red' in x.values())

d = json.loads('[1,{"c":"red","b":2},3]')
print s(d)

print s(data)
