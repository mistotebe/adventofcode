#!/usr/bin/env python

total = 100

splits = lambda : ((a, b, c, 100 - (a + b + c)) for a in range(total + 1) for b in range(0, total + 1 - a) for c in range(0, total + 1 - (a + b)))

i = [
    # Sprinkles
    {
        "capacity": 2,
        "durability": 0,
        "flavor": -2,
        "texture": 0,
        "calories": 3,
    },
    # Butterscotch
    {
        "capacity": 0,
        "durability": 5,
        "flavor": -3,
        "texture": 0,
        "calories": 3,
    },
    # Chocolate
    {
        "capacity": 0,
        "durability": 0,
        "flavor": 5,
        "texture": -1,
        "calories": 8,
    },
    # Candy
    {
        "capacity": 0,
        "durability": -1,
        "flavor": 0,
        "texture": 5,
        "calories": 8,
    },
]

import operator

v = lambda x: {k: x[0]*v for k, v in x[1].iteritems()}
m = lambda l: {k: max(0, sum(map(operator.itemgetter(k), l))) for k in l[0]}

d = lambda x: (v for k, v in x.iteritems() if k != 'calories')

print max(reduce(operator.mul, d(x)) for x in (m(map(v, zip(recipe, i))) for recipe in splits()))
print max(reduce(operator.mul, d(x)) for x in (m(map(v, zip(recipe, i))) for recipe in splits()) if x['calories'] == 500)
