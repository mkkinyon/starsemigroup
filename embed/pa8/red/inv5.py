"""What does the x-link buy?  Clauses over (y; a, c, b) valid under the full (W_2) hypotheses but not without x.  Usage: python3 inv5.py m K"""
import sys, time, itertools, pickle
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
m = int(sys.argv[1]); K = int(sys.argv[2])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
V = ['y', 'a', 'c', 'b']
atoms = [('E', p) for p in V] + [('T', p, 'u') for p in V] + [('T', p, 'v') for p in V] + [('J', p, q) for p in V for q in V if p < q]
lits = [(s, a) for a in atoms for s in (1, -1)]
def lit_val(c, u, v, lit):
    s, a = lit
    if a[0] == 'E': x = c.E(c.i[a[1]], u, v)
    elif a[0] == 'T': x = c.Tl(c.i[a[1]], u if a[2] == 'u' else v)
    else: x = c.J(c.i[a[1]], c.i[a[2]], u, v)
    return s * x
def fmt(cl):
    def f(lit):
        s, a = lit
        t = f"E({a[1]})" if a[0] == 'E' else (f"T({a[1]},{a[2]})" if a[0] == 'T' else f"J({a[1]}{a[2]})")
        return t if s > 0 else '~' + t
    return ' | '.join(f(l) for l in cl)
class Ctx: pass
def run(H, goal):
    T, idx = table(H, ('mt', 'a', 'b'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in V}; ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in goal: cls.append([-w_, -lit_val(c, u, v, l)])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
def clauses():
    for k in range(1, K + 1):
        for cl in itertools.combinations(lits, k):
            if len({a for s, a in cl}) < k: continue
            yield cl
def subsumed(cl, S):
    s = set(cl); return any(set(c2) <= s and len(c2) < len(cl) for c2 in S)
W2 = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
weak = [('mt','a','c'), ('mt','c','b'), idf('y'), ('comm','y','b')]
t0 = time.time(); S = []; n = 0
for cl in clauses():
    n += 1
    if subsumed(cl, S): continue
    if run(W2, cl): S.append(cl)
print(f"{len(S)} minimal valid clauses under (W_2), {n} tested ({time.time()-t0:.0f}s)", flush=True)
new = [cl for cl in S if not run(weak, cl)]
print(f"{len(new)} of them fail without the x-link:", flush=True)
for cl in new: print('   ', fmt(cl))
pickle.dump((S, new), open(f'inv5_m{m}_K{K}.pkl', 'wb'))
