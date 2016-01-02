#!/usr/bin/env python

c = set()

import ply.lex as lex

tokens = (
    "NAME",
    "WOULD",
    "VALUE",
    "EOL",
    "BY",
)

t_NAME = r"[A-Z][a-z]*"
t_WOULD = r"would"
t_EOL = r"\n"
t_BY = r"happiness\ units\ by\ sitting\ next\ to"

def t_VALUE(t):
    r"(gain|lose)\ [0-9]+"
    sign, num = t.value.split()
    t.value = int(num)
    if sign == 'lose':
        t.value *= -1
    return t

t_ignore = ' .'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

import ply.yacc as yacc

class Parser(object):
    tokens = tokens
    start = 'distances'

    def p_distances(self, p):
        """distances : distances distance"""
        d = p[1]
        k, v = p[2]
        d[k] = v
        p[0] = d

    def p_distances_stop(self, p):
        """distances :"""
        p[0] = {}

    def p_distance(self, p):
        """distance : NAME WOULD VALUE BY NAME EOL"""
        c.add(p[1])
        p[0] = ((p[1], p[5]), p[3])

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


data = open("day13.in").read()

def distance(g, p):
    #print p
    d = 0
    s, rest = p[0], list(p[1:])
    rest.append(s)
    l = s
    for n in rest:
        #print "%s -> %s = %d" % (l, n, g[(l, n)] + g[(n, l)])
        #print g[(l, n)],
        d += g[(l, n)] + g[(n, l)]
        l = n
    #print "=", d
    return d

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    distances = parser.parse(data, lexer=lexer, debug=False)
    #print distances
    import itertools
    guests = list(c)
    result = max(distance(distances, path) for path in itertools.permutations(guests))
    print result
    me = 'me'
    for g in guests:
        distances[(me, g)] = 0
        distances[(g, me)] = 0
    result = max(distance(distances, (me,) + path) for path in itertools.permutations(guests))
    print result
