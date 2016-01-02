#!/usr/bin/env python

c = set()

import ply.lex as lex

tokens = (
    "SUE",
    "ITEM",
    "COLON",
    "COMMA",
    "EOL",
    "NUM",
)

t_SUE = r"Sue"
t_ITEM = r"[a-z]+"
t_COLON = r":"
t_COMMA = r","
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
    start = 'aunts'

    def p_aunts(self, p):
        """aunts : aunts aunt"""
        p[1].update(p[2])
        p[0] = p[1]

    def p_aunts_stop(self, p):
        """aunts :"""
        p[0] = {}

    def p_aunt(self, p):
        """aunt : SUE NUM COLON knowledge EOL"""
        p[0] = {p[2]: p[4]}

    def p_knowledge(self, p):
        """knowledge : knowledge COMMA item"""
        p[1].update(p[3])
        p[0] = p[1]

    def p_knowledge_stop(self, p):
        """knowledge : item"""
        p[0] = p[1]

    def p_item(self, p):
        """item : ITEM COLON NUM"""
        p[0] = {p[1]: int(p[3])}

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


data = open("day16.in").read()

scan = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

def check1(a):
    for i in a:
        if scan[i] != a[i]:
            return False
    return True

import operator
d = {'cats': -1,
     'trees': -1,
     'pomeranians': 1,
     'goldfish': 1,
}

def check2(a):
    for i in a:
        if cmp(scan[i], a[i]) != d.get(i, 0):
            return False
    return True

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    aunts = parser.parse(data, lexer=lexer, debug=False)
    print { k: v for k, v in aunts.iteritems() if check1(v) }
    print { k: v for k, v in aunts.iteritems() if check2(v) }
