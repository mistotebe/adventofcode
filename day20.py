#!/usr/bin/env python3

import sys
import math

class Primes(object):
    p = [2, 3]

    def __init__(self):
        self.candidate = self.p[-1] + 1
        self.root = math.floor(math.sqrt(self.candidate))
        self.counter = self.root*(self.root + 2) - self.candidate

    def __iter__(self):
        for p in self.p:
            yield p
        yield from self._primes()

    def _next_c(self):
        r = self.candidate
        self.candidate += 1
        if self.counter:
            self.counter -= 1
        else:
            self.root += 1
            self.counter = 2 * self.root
        return r

    def _primes(self):
        while True:
            for p in self.p:
                if self.candidate % p == 0:
                    break
                elif p > self.root:
                    self.p.append(self.candidate)
                    yield self.candidate
                    break
            self.candidate += 1
            if self.counter:
                self.counter -= 1
            else:
                self.root += 1
                self.counter = 2 * self.root

l = [0, 1]

def presents1():
    primes = Primes()
    yield from enumerate(l)
    i = len(l)
    while True:
        # invariant: c*x = i
        c, x = i, 1
        for p in primes:
            if not i % p:
                break
            if p > math.sqrt(i):
                p = c
                break
        # c mod p == 0
        while c % p == 0:
            c //= p
            x *= p
        if c == 1:
            # x = p*n
            r = (p*x - 1)//(p - 1)
        else:
            # x and c are coprime
            r = l[c]*l[x]
        l.append(r)
        yield i, r
        i += 1

target = 3400000

for pos, s in presents1():
    if s >= target:
        print(pos)
        break

for pos in range(1,5000000):
    s = 0
    for x in range(1, 51):
        if not pos % x:
            s += 11 * (pos // x)
    if s > 10*target:
        print(pos)
        break
