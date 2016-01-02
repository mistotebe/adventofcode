#!/usr/bin/env python

from collections import namedtuple
from functools import partial
from itertools import starmap

Item = namedtuple('Item', ['cost', 'damage', 'armor'])
Gear = namedtuple('Gear', ['weapon', 'armor', 'left_ring', 'right_ring'])
Outcome = namedtuple('Outcome', ['won', 'cost', 'health_left', 'gear'])

# you must buy exacly one weapon
weapons = list(starmap(Item, [
    (8, 4, 0,),
    (10, 5, 0,),
    (25, 6, 0,),
    (40, 7, 0,),
    (74, 8, 0,),
]))

armor = list(starmap(Item, [
    (0, 0, 0,),
    (13, 0, 1,),
    (31, 0, 2,),
    (53, 0, 3,),
    (75, 0, 4,),
    (102, 0, 5,),
]))

rings = list(starmap(Item, [
    (0, 0, 0,),
    (25, 1, 0,),
    (50, 2, 0,),
    (100, 3, 0,),
    (20, 0, 1,),
    (40, 0, 2,),
    (80, 0, 3,),
]))

choices = lambda: (Gear(w, a, r1, r2) for w in weapons for a in armor for r1 in rings for r2 in rings if (r1 < r2 or r1 == Item(0, 0, 0)))

def f(h, b, e):
    c, d, a = (sum(x._asdict()[y] for x in e) for y in ['cost', 'damage', 'armor'])
    bh, bd, ba = b
    #print "Me", h, d, a
    #print "Boss", bh, bd, ba

    while bh > 0 and h > 0:
        #print "I hit for", max(1, d - ba),
        bh -= max(1, d - ba)
        #print bh, "remains"
        if bh <= 0:
            return Outcome(True, c, h, e)
        #print "Boss hits for", max(1, bd - a),
        h -= max(1, bd - a)
        #print h, "remains"
    return Outcome(False, c, h, e)

h = 100
boss = (100, 8, 2)

print min(x for x in map(partial(f, h, boss), choices()) if x.won)
print max(x for x in map(partial(f, h, boss), choices()) if not x.won)
