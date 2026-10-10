"""Test path-closing hypothesis sets (from pathclose.py) on given projection-algebra tables."""
import sys, json, itertools, glob
from mace4parse import parse_models

def violations(A, n, combo, distinct=True):
    """combo: list of atoms; returns instances (P, x) satisfying path + atoms with p0 !~ pn"""
    N = len(A); th = lambda p, q: A[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    matched = {p: [q for q in range(N) if mt(p, q)] for p in range(N)}
    def hold(at, P, x):
        k = at[0]
        if k == 'comm': return th(x, P[at[1]]) == th(P[at[1]], x)
        if k == 'xle': return th(P[at[1]], x) == x
        if k == 'lex': return th(x, P[at[1]]) == P[at[1]]
        if k == 'sees': return th(x, P[at[1]]) == th(x, P[at[2]])
        if k == 'seen': return th(P[at[1]], x) == th(P[at[2]], x)
        if k == 'xeq': return th(P[at[1]], P[at[2]]) == x
    out = []
    def paths(prefix):
        if len(prefix) == n + 1:
            yield prefix; return
        for q in matched[prefix[-1]]:
            yield from paths(prefix + [q])
    for p0 in range(N):
        for P in paths([p0]):
            if mt(P[0], P[-1]): continue
            if distinct and len(set(P)) < len(P): continue
            for x in range(N):
                if distinct and x in P: continue
                if all(hold(at, P, x) for at in combo): out.append((tuple(P), x))
    return out

def algebras():
    """named list of (name, table) for the test bed"""
    out = []
    for l in open('pa7_post.log'):
        r = json.loads(l); out.append(('o7-' + ('emb' if r['embeds'] else 'P7'), r['A']))
    for N, T, c in parse_models(open('pa_6_user.out').read()): out.append(('o6', T))
    from fourth import table as P7
    P9names = 'a b c d m n k w z'.split()
    rows = '''a m a m m m m w w
m b b b m m m w w
c c c z n n z z z
k d z d k z k z z
m m m m m m m w w
n n n z n n z z z
k k z k k z k z z
w w w w w w w w w
z z z z z z z z z'''.split('\n')
    thP9 = {p: dict(zip(P9names, r.split())) for p, r in zip(P9names, rows)}
    out.append(('P9', [[P9names.index(thP9[q][p]) for q in P9names] for p in P9names]))
    import pickle
    Tq, sq, A2 = pickle.load(open('hex_smallest.pkl', 'rb'))
    from layered import proj_algebra
    P, A = proj_algebra(list(range(len(Tq))), Tq, sq); out.append(('P(Q0)', A))
    return out

if __name__ == "__main__":
    n = int(sys.argv[1]); combos = json.loads(sys.argv[2])
    algs = algebras()
    for combo in combos:
        combo = [tuple(a) for a in combo]
        bad = {}
        for name, A in algs:
            v = violations(A, n, combo)
            if v: bad[name] = bad.get(name, 0) + 1
        print(combo, '-> violated in:', bad if bad else 'none')
