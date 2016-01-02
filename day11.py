#!/usr/bin/env python

def increment(s, p=-1, c='z'):
    l = len(s)
    if p != -1:
        l = p+1
    for i in reversed(range(l)):
        if s[i] == 'z' or (i == p and s[i] >= c):
            continue
        elif i == p and s[i] < c:
            return s[:i] + c + 'a'*(len(s) - i - 1)
        return s[:i] + chr(ord(s[i]) + 1) + 'a'*(len(s) - i - 1)

def rule1(s):
    def check(s):
        rest = s
        while len(rest) >= 3:
            a, b, c = rest[:3]
            if ord(c) - ord(b) == 1 and ord(b) - ord(a) == 1:
                return -1, None
            rest = rest[1:]
        if ord(b) - ord(a) == 1:
            # s[-3] and s[-2] are fine, advance s[-1]
            return len(s) - 1, chr(ord(b) + 1)
        # advance s[-2] to follow s[-3]
        if a == 'z':
            return len(s) - 2, 'a'
        return len(s) - 2, chr(ord(a) + 1)

    p, c = check(s)
    while c is not None:
        s = increment(s, p, c)
        p, c = check(s)
    return s

def rule2(s):
    def check(s):
        i = -1
        for c in 'ilo':
            p = s.find(c)
            if p != -1 and (i == -1 or p < i):
                i = p
        return i, chr(ord(s[i]) + 1)

    p, c = check(s)
    while p != -1:
        s = increment(s, p, c)
        p, c = check(s)

    return s

def rule3(s):
    def check(s):
        c1, rest = s[0], s[1:]
        while rest and c1 != rest[0]:
            c1, rest = rest[0], rest[1:]
        if len(rest) <= 2:
            return len(s) - 3, s[-4]
        c2, rest = rest[1], rest[2:]
        while len(rest) > 1 and (c1 == c2 or c2 != rest[0]):
            c2, rest = rest[0], rest[1:]
        if c2 == rest[0]:
            return len(s) - 1, None
        return len(s) - 1, c2

    p, c = check(s)
    while c is not None:
        s = increment(s, p, c)
        p, c = check(s)

    return s

pwd = 'vzbxkghb'
#pwd = 'abcdefgh'
#pwd = 'ghijklmn'
pwd = increment('vzbxxyzz')

succ = lambda s: max(x(s) for x in (rule1, rule2, rule3))

if __name__ == '__main__':
    print pwd
    old, new = '', pwd
    while old != new:
        old, new = new, succ(new)
    print new
