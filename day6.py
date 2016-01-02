#!/usr/bin/env python

p1 = {
    'toggle': lambda x: not x,
    'turn on': lambda x: True,
    'turn off': lambda x: False,
}

p2 = {
    'toggle': lambda x: x + 2,
    'turn on': lambda x: x + 1,
    'turn off': lambda x: x and x - 1,
}

class Operation(object):
    def __init__(self, op, start, end):
        self.op = op
        self.x = xrange(start[0], end[0]+1)
        self.y = xrange(start[1], end[1]+1)

    def __call__(self, a):
        for x, y in ((x, y) for x in self.x for y in self.y):
            a[x][y] = self.op(a[x][y])
        return a

import ply.lex as lex

tokens = (
    "THROUGH",
    "COMMA",
    "NUM",
    "EOL",
    "UP",
    "DOWN",
    "TOGGLE",
)

t_THROUGH = r"through"
t_COMMA = r","
t_NUM = r"[0-9]+"
t_EOL = r"\n"
t_UP = r"turn\ on"
t_DOWN = r"turn\ off"
t_TOGGLE = r"toggle"

t_ignore = ' '

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

import ply.yacc as yacc

class Parser(object):
    tokens = tokens
    start = 'instructions'

    # instructions -> instruction*
    def p_instructions(self, p):
        """instructions : instructions instruction"""
        p[0] = p[2](p[1])

    def p_instructions_stop(self, p):
        """instructions :"""
        p[0] = [[False]*1000 for x in xrange(1000)]

    # instruction -> op coord "through" coord EOL
    def p_instruction(self, p):
        """instruction : op coord THROUGH coord EOL"""
        p[0] = Operation(p[1], p[2], p[4])

    def p_op(self, p):
        """op : UP
              | DOWN
              | TOGGLE"""
        d = p2
        p[0] = d[p[1]]

    # coord : NUM COMMA NUM
    def p_coord(self, p):
        """coord : NUM COMMA NUM"""
        p[0] = (int(p[1]), int(p[3]))

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


data = open("day6.in").read()

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    result = parser.parse(data, lexer=lexer, debug=False)
    print sum((int(point) for line in result for point in line if point))
