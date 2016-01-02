#!/usr/bin/env python

import ply.lex as lex

class Tokenizer(object):
    tokens = (
        'E',
        'ATOM',
    )

    t_E = "e"
    t_ATOM = "[A-Z][a-z]?"

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
        raise SyntaxError(message)

tokenizer = lex.lex(module=Tokenizer())
