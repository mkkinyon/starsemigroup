"""Write DIMACS CNF files for the SAT validity checks, for an external solver (kissat).
A condition is valid in P(P_m) iff every file it produces is UNSATISFIABLE.
Usage: python3 dump.py NAME m      NAME in W2 W3 W4 Rpp Rp2 Rp3 lemA"""
import sys, os
os.environ['PA_SAT_DUMP'] = f"{sys.argv[1]}_m{sys.argv[2]}"; os.environ['PA_SAT_DUMP_N'] = '0'
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
P = [('mt','a','c'), ('mt','c','b')]
def chain(xs, last):   # c ~ x1 ~ ... ~ xn (~ b if last), each identifying a with c
    at = [('comm', xs[0], 'c')] + [('comm', u, v) for u, v in zip(xs, xs[1:])] + [('eq', (x, 'a'), (x, 'c')) for x in xs]
    return at + ([('comm', xs[-1], 'b')] if last else [])
H = {
 'W2':  P + chain(['x','y'], True),
 'W3':  P + chain(['x','y','z'], True),
 'W4':  P + chain(['x','y','z','t'], True),
 'Rpp': P + [('comm','x','c'), ('eq',('x','a'),('x','c')), ('comm','y','b'), ('eq',('x','b'),('y','a'))],
 'Rp2': P + chain(['x','z'], False) + [('comm','y','a'), ('eq',('z','b'),('y','b'))],
 'Rp3': P + chain(['x','z','t'], False) + [('comm','y','a'), ('eq',('t','b'),('y','b'))],
}
valid(H[sys.argv[1]], ('mt','a','b'), int(sys.argv[2]))
