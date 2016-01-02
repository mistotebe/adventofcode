#!/usr/bin/env python

c = set()

import ply.lex as lex

tokens = (
    "CITY",
    "TO",
    "EQUALS",
    "EOL",
    "NUM",
)

t_CITY = r"[A-Z][A-Za-z]*"
t_TO = r"to"
t_EQUALS = r"="
t_EOL = r"\n"
t_NUM = r"[0-9]+"

t_ignore = ' '

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
        d[frozenset(k)] = v
        p[0] = d

    def p_distances_stop(self, p):
        """distances :"""
        p[0] = {}

    def p_distance(self, p):
        """distance : CITY TO CITY EQUALS NUM EOL"""
        c.add(p[1])
        c.add(p[3])
        p[0] = ({p[1], p[3]}, int(p[5]))

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


data = open("day9.in").read()

def distance(g, p):
    #print p
    d = 0
    l, rest = p[0], p[1:]
    for n in rest:
        #print "%s -> %s = %d" % (l, n, g[frozenset({l, n})])
        #print g[frozenset({l, n})],
        d += g[frozenset({l, n})]
        l = n
    #print "=", d
    return d

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    distances = parser.parse(data, lexer=lexer, debug=False)
    print distances
    import itertools
    result = min(distance(distances, path) for path in itertools.permutations(c))
    print result
    result = max(distance(distances, path) for path in itertools.permutations(c))
    print result
