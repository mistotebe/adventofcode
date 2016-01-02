#!/usr/bin/env python

import ply.lex as lex

d = {'Mg': 'MG', 'B': 'B', 'F': 'F', 'H': 'H', 'Ca': 'CA', 'C': 'C', 'O': 'O', 'Al': 'AL', 'P': 'P', 'Si': 'SI', 'Ar': 'AR', 'Th': 'TH', 'Ti': 'TI', 'Y': 'Y', 'Rn': 'RN', 'N': 'N', 'e': 'E'}
tokens = ['DUMMY'] + d.values()

def t_DUMMY(t):
    r"[A-Z][a-z]?"
    t.type = d[t.value]
    return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    raise SyntaxError(message)

lexer = lex.lex()

replacements = """
al : th f
al : th rn f ar
b : b ca
b : ti b
b : ti rn f ar
ca : ca ca
ca : p b
ca : p rn f ar
ca : si rn f y f ar
ca : si rn mg ar
ca : si th
f : ca f
f : p mg
f : si al
h : c rn al ar
h : c rn f y f y f ar
h : c rn f y mg ar
h : c rn mg y f ar
h : h ca
h : n rn f y f ar
h : n rn mg ar
h : n th
h : o b
h : o rn f ar
mg : b f
mg : ti mg
n : c rn f ar
n : h si
o : c rn f y f ar
o : c rn mg ar
o : h p
o : n rn f ar
o : o ti
p : ca p
p : p ti
p : si rn f ar
si : ca si
th : th ca
ti : b p
ti : ti ti
e : h f
e : n al
e : o mg
"""

terminals = """
mg : MG
b : B
f : F
c : C
h : H
ca : CA
al : AL
o : O
n : N
p : P
si : SI
ar : AR
th : TH
ti : TI
y : Y
rn : RN
e : E
"""

class P(object):
    tokens = tokens
    count = 0
    start = 'e'

    def p_error(self, p):
        message = "Syntax error in input! %s" % p
        import ipdb; ipdb.set_trace()
        print message
        raise SyntaxError(message)

p = P()

n = 0

for r in replacements.split('\n'):
    if not r: continue
    def f(p):
        p[0] = 1 + sum(p[1:])
    name = 'p_' + r.split()[0] + str(n)
    f.__name__ = name
    f.__doc__ = r
    n+=1
    p.__setattr__(name, f)

for t in terminals.split('\n'):
    if not t: continue
    def f(p):
        p[0] = 0
    name = 'p_' + t.split()[0] + str(n)
    f.__name__ = name
    f.__doc__ = t
    n+=1
    p.__setattr__(name, f)

import ply.yacc as yacc

parser = yacc.yacc(module=p)

s = 'CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl'

print parser.parse(s, lexer=lexer, debug=False)
