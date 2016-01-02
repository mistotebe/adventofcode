#!/usr/bin/env python

import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('f', nargs='?', type=argparse.FileType('r'), default=open('day7.in'))

class Op(object):
    bits = 16
    bound = 1 << bits

    def __init__(self, *args):
        self.deps = args

    def resolve(self, name, cache=None):
        if cache is None:
            cache = {}
        if cache.get(name) is None:
            cache[name] = self.op(cache)
        return cache

class Ops(object):
    def __init__(self, items):
        self.ops = dict(items)

    def resolve(self, name, cache=None):
        if cache is None:
            cache = {}
        if isinstance(name, int):
            cache[name] = name
        else:
            self.ops[name].resolve(name, cache)
        return cache

class Set(Op):
    def __init__(self, value):
        super(Set, self).__init__()
        self.value = value

    def op(self, cache=None):
        ops.resolve(self.value, cache=cache)
        return cache[self.value]

class Not(Op):
    def op(self, cache=None):
        dep = self.deps[0]
        ops.resolve(dep, cache=cache)
        return ~cache[dep] % self.bound

class And(Op):
    def op(self, cache=None):
        left, right = self.deps
        ops.resolve(left, cache=cache)
        ops.resolve(right, cache=cache)
        return cache[left] & cache[right]

class Or(Op):
    def op(self, cache=None):
        left, right = self.deps
        ops.resolve(left, cache=cache)
        ops.resolve(right, cache=cache)
        return cache[left] | cache[right]

class LShift(Op):
    def __init__(self, dep, value):
        super(LShift, self).__init__(dep)
        self.value = value

    def op(self, cache=None):
        dep = self.deps[0]
        ops.resolve(dep, cache=cache)
        return (cache[dep] << self.value) % self.bound

class RShift(Op):
    def __init__(self, dep, value):
        super(RShift, self).__init__(dep)
        self.value = value

    def op(self, cache=None):
        dep = self.deps[0]
        ops.resolve(dep, cache=cache)
        return cache[dep] >> self.value


import ply.lex as lex

tokens = (
    "ID",
    "NUM",

    "TO",
    "EOL",

    "AND",
    "OR",
    "NOT",
    "LSHIFT",
    "RSHIFT",
)

t_ID = r"[a-z]+"
t_NUM = r"[0-9]+"

t_TO = r"->"
t_EOL = r"\n"

t_AND = r"AND"
t_OR = r"OR"
t_NOT = r"NOT"
t_LSHIFT = r"LSHIFT"
t_RSHIFT = r"RSHIFT"

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
        p[0] = p[1] + [p[2]]

    def p_instructions_stop(self, p):
        """instructions :"""
        p[0] = []

    def p_instruction(self, p):
        """instruction : op TO ID EOL"""
        p[0] = (p[3], p[1])

    def p_op(self, p):
        """op : num
              | or
              | and
              | not
              | lshift
              | rshift"""
        p[0] = p[1]

    def p_expr_id(self, p):
        """EXPR : ID"""
        p[0] = p[1]

    def p_expr_num(self, p):
        """EXPR : NUM"""
        p[0] = int(p[1])

    def p_or(self, p):
        """or : EXPR OR EXPR"""
        p[0] = Or(p[1], p[3])

    def p_and(self, p):
        """and : EXPR AND EXPR"""
        p[0] = And(p[1], p[3])

    def p_not(self, p):
        """not : NOT EXPR"""
        p[0] = Not(p[2])

    def p_lshift(self, p):
        """lshift : EXPR LSHIFT NUM"""
        p[0] = LShift(p[1], int(p[3]))

    def p_rshift(self, p):
        """rshift : EXPR RSHIFT NUM"""
        p[0] = RShift(p[1], int(p[3]))

    def p_num(self, p):
        """num : EXPR"""
        p[0] = Set(p[1])

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


options = argparser.parse_args()

data = options.f.read()

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    result = parser.parse(data, lexer=lexer, debug=0)
    ops = Ops(result)
    cache = ops.resolve('a')
    a = cache['a']
    cache = ops.resolve('a', {'b': a})
    print cache
    print cache['a']
