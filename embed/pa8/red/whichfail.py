"""Evaluate clauses (inv4 S1/S3 language) on a concrete (a,c,y) configuration and list which fail."""
import sys, pickle, itertools
import re
def parse(s):   # "[0 2] [1 3] (4)" -> blocks list [(set, 'T'/'N')]
    return [(set(int(p) for p in body.split()), 'T' if op == '[' else 'N') for op, body in re.findall(r'([\[\(])([^\]\)]*)[\]\)]', s)]
def mkpart(blocks):
    return blocks
def blk(P, u):
    for pts, k in P:
        if u in pts: return pts, k
def E(P, u, v): return blk(P, u)[0] == blk(P, v)[0]
def T(P, u): return blk(P, u)[1] == 'T'
def join(Ps, X):
    parent = {u: u for u in X}
    def f(u):
        while parent[u] != u: u = parent[u]
        return u
    for P in Ps:
        for pts, k in P:
            pts = sorted(pts)
            for p in pts[1:]: parent[f(p)] = f(pts[0])
    return lambda u, v: f(u) == f(v)
def evaluate(conf, X, clauses, fmt):
    a, c, y = conf['a'], conf['c'], conf['x']
    J = {('a','c'): join([a, c], X), ('a','x'): join([a, y], X), ('c','x'): join([c, y], X)}
    J3 = join([a, c, y], X)
    P = {'a': a, 'c': c, 'x': y}
    def lit(l, u, v):
        s, at = l
        if at[0] == 'E': val = E(P[at[1]], u, v)
        elif at[0] == 'T': val = T(P[at[1]], u if at[2] == 'u' else v)
        elif at[0] == 'J': val = J[(at[1], at[2])](u, v)
        else: val = J3(u, v)
        return val if s > 0 else not val
    fails = []
    for cl in clauses:
        for u in X:
            for v in X:
                if u != v and not any(lit(l, u, v) for l in cl): fails.append((cl, u, v)); break
            else: continue
            break
    return fails
if __name__ == '__main__':
    sys.argv = ['x', '5', '4']
    src = open('inv4.py').read().split("if __name__ == '__main__':")[0]
    exec(src.split("class Ctx: pass")[0])   # atoms, fmt
    S1, S2, S3 = pickle.load(open('inv4_m4_K4.pkl', 'rb'))
    conf = {'a': parse("[0 2] [1 3] (4)"), 'c': parse("(0) (1) [2] [3 4]"), 'x': parse("(0 1) [2 4] [3]")}
    X = range(5)
    fails = evaluate(conf, X, S3, fmt)
    print(len(fails), "of", len(S3), "chain-valid (m=4) clauses fail on the counterexample (y in the role of x):")
    for cl, u, v in fails: print('   ', fmt(cl), f"  at u={u}, v={v}")
