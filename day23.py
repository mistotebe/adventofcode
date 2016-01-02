#!/usr/bin/env python

class Instruction(object):
    def __init__(self, operand=False, offset=1):
        self.operand = operand
        self.offset = offset

    def process(self, state):
        return 1

class Half(Instruction):
    def process(self, state):
        state[self.operand] //= 2
        return super(Half, self).process(state)

class Triple(Instruction):
    def process(self, state):
        state[self.operand] *= 3
        return super(Triple, self).process(state)

class Increment(Instruction):
    def process(self, state):
        state[self.operand] += 1
        return super(Increment, self).process(state)

class Jump(Instruction):
    def __init__(self, offset=1, operand=False, condition=lambda *x: True):
        self.condition = condition
        super(Jump, self).__init__(offset=offset, operand=operand)

    def process(self, state):
        if self.condition(state, self.operand):
            return self.offset
        return super(Jump, self).process(state)

class Program(object):
    def __init__(self, instructions):
        self.instructions = instructions

    def run(self, state=None):
        o = 0
        if state is None:
            state = { i.operand : 0 for i in self.instructions if i.operand }
        while o in range(len(self.instructions)):
            o += self.instructions[o].process(state)
        return state

import ply.lex as lex

tokens = (
    "ID",
    "NUM",

    "HLF",
    "TPL",
    "INC",
    "JMP",
    "JIO",
    "JIE",
)

t_ID = r"[ab]"

t_HLF = r"hlf"
t_TPL = r"tpl"
t_INC = r"inc"
t_JMP = r"jmp"
t_JIO = r"jio"
t_JIE = r"jie"

def t_NUM(t):
    r"[+-]?[0-9]+"
    t.value = int(t.value)
    return t

t_ignore = ' ,\n'

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

    def p_op_hlf(self, p):
        """instruction : HLF ID"""
        p[0] = Half(p[2])

    def p_op_tpl(self, p):
        """instruction : TPL ID"""
        p[0] = Triple(p[2])

    def p_op_inc(self, p):
        """instruction : INC ID"""
        p[0] = Increment(p[2])

    def p_op_jmp(self, p):
        """instruction : JMP NUM"""
        p[0] = Jump(offset=p[2])

    def p_op_jio(self, p):
        """instruction : JIO ID NUM"""
        p[0] = Jump(condition=lambda state, operand: state[operand] == 1, operand=p[2], offset=p[3])

    def p_op_jie(self, p):
        """instruction : JIE ID NUM"""
        p[0] = Jump(condition=lambda state, operand: state[operand] % 2 == 0, operand=p[2], offset=p[3])

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)


data = open('day23.in').read()

if __name__ == "__main__":
    parser = yacc.yacc(module=Parser())
    result = parser.parse(data, lexer=lexer, debug=0)
    p = Program(result)
    state = p.run()
    print state
    state = p.run({'a': 1, 'b': 0})
    print state
