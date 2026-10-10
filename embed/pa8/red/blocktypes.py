"""Types of y-blocks relative to (a, c) on the (W_2) instances in P_4 (y = second chain element), compared with x-blocks (first element)."""
import sys, pickle, itertools
from collections import Counter
sys.path.insert(0, '/home/claude/pa8w/embed')
n = 4
inst = pickle.load(open('../rpp/w2inst4.pkl', 'rb'))
def blocks(p):   # pmon partition -> list of (set of top points, 'T'/'N')
    out = []
    for b in p:
        top = {i for i in b if i < n}
        if top: out.append((top, 'T' if any(i >= n for i in b) else 'N'))
    return out
def part(p): return [bl for bl, k in blocks(p)]
def supp(p): return set().union(*[bl for bl, k in blocks(p) if k == 'T']) if any(k == 'T' for bl, k in blocks(p)) else set()
def classes(parts):
    parent = {u: u for u in range(n)}
    def f(u):
        while parent[u] != u: u = parent[u]
        return u
    for P in parts:
        for bl in P:
            bl = sorted(bl)
            for q in bl[1:]: parent[f(q)] = f(bl[0])
    return lambda u, v: f(u) == f(v)
def sig(Y, kind, a, c):
    """signature of a block Y of the chain element relative to a, c"""
    Sa, Sc = supp(a), supp(c)
    Jac = classes([part(a), part(c)])
    cb = part(c); ab = part(a)
    inside_c_block = any(Y <= bl for bl in cb)
    union_of_c = all((bl <= Y) or not (bl & Y) for bl in cb)
    in_class_ac = all(Jac(u, v) for u in Y for v in Y)
    meets_Sc = bool(Y & Sc); inside_Sc = Y <= Sc
    meets_Sa = bool(Y & Sa); inside_Sa = Y <= Sa
    meets_a_minus_c = bool(Y & (Sa - Sc))
    n_cT = sum(1 for bl, k in blocks(c) if k == 'T' and bl & Y)
    n_cN = sum(1 for bl, k in blocks(c) if k == 'N' and bl & Y)
    return (kind, 'inC' if inside_c_block else ('unionC' if union_of_c else 'mixC'), 'inGamma' if in_class_ac else 'splitAC',
            'Sc:' + ('in' if inside_Sc else ('meet' if meets_Sc else 'no')), 'Sa:' + ('in' if inside_Sa else ('meet' if meets_Sa else 'no')),
            'a-c' if meets_a_minus_c else '-', f'#cT={n_cT}', f'#cN={n_cN}')
cnt_x = Counter(); cnt_y = Counter(); ex = {}
for a, c, b, x, y in inst:
    for Y, k in blocks(x): cnt_x[sig(Y, k, a, c)] += 1
    for Y, k in blocks(y):
        s = sig(Y, k, a, c); cnt_y[s] += 1
        if s not in ex: ex[s] = (a, c, x, y)
print("x-block types (c~x, x id):"); [print('  ', s, v) for s, v in sorted(cnt_x.items())]
print("y-block types (c~x~y, both id):"); [print('  ', s, v, '' if s in cnt_x else '  <-- NEW') for s, v in sorted(cnt_y.items())]
pickle.dump(ex, open('blocktypes_ex.pkl', 'wb'))
