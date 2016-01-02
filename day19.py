#!/usr/bin/env python

from collections import defaultdict

import ply.lex as lex

tokens = (
    "NAME",
    "TO",
    "EOL",
)

class Lexer(object):
    tokens = tokens

    t_NAME = r"[a-zA-Z0-9]+"
    t_TO = r"=>"
    t_EOL = r"\n"

    t_ignore = ' '

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
        raise SyntaxError(message)

lexer = lex.lex(module=Lexer())

from day18_t import tokenizer

import ply.yacc as yacc

nonterminals = set()
ts = set()

class Parser(object):
    tokens = tokens
    start = 'description'

    def p_description(self, p):
        """description : replacements EOL NAME EOL"""
        d = p[1]
        m = p[3]
        p[0] = (d, m)

    def p_replacements(self, p):
        """replacements : replacements replacement"""
        d = p[1]
        k, v = p[2]
        d[k].append(v)
        p[0] = d

    def p_replacements_stop(self, p):
        """replacements : """
        p[0] = defaultdict(list)

    def p_replacement(self, p):
        """replacement : NAME TO NAME EOL"""
        nonterminals.add(p[1])

        tokenizer.input(p[3])
        for t in tokenizer:
            ts.add(t.value)

        p[0] = (p[1], p[3])

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


data = open("day18.in").read()

def step(r, m):
    o = set()
    for x in m:
        for y in r:
            i = 0
            while x.find(y, i) != -1:
                i = x.find(y, i)
                for c in r[y]:
                    o.add(x[:i] + c + x[(i+len(y)):])
                i += 1
    return o

def prune(s, molecule):
    if len(s) > len(molecule):
        return False
    for u in bounded:
        if s.count(u) > molecule.count(u):
            return False
    return True

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    a = c = {'e'}
    s = 0
    molecule, replacements = 'HOHOHO', {
            'e': ['O', 'H'],
            'O': ['HH'],
            'H': ['OH', 'HO'],
    }
    replacements, molecule = parser.parse(data, lexer=lexer, debug=False)
    print replacements, molecule
    print ts
    print repr({x: x.upper() for x in ts})
    bounded = list(ts - nonterminals) + ['Th', 'Si']
    f = lambda x: prune(x, molecule)
    while False and molecule not in c:
        s += 1
        old = c
        #print s, c, step(replacements, c)
        c = set(filter(f, step(replacements, c))) - a
        a |= c
    for x in ts:
        print x.lower(), ':', x.upper()
    print s
