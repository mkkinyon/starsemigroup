"""Does T1 follow from local two-point statements about (x; a, b, c) valid under a|><|c, c~x, x id, x~b?  Pool: clauses of <= K literals over
atoms E(p), T(p,u), T(p,v), J(pq), J3(pqr) for p,q,r in {x,a,b,c}.  Usage: python3 t1loc.py m K"""
import sys, time, itertools, pickle
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2]]
m = int(sys.argv[1]); K = int(sys.argv[2])
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
exec(open('inv4.py').read().split("def run(H, hyps, goal):")[0].split("class Ctx: pass")[1])   # make_J3
class Ctx: pass
V = ['x', 'a', 'b', 'c']
TR = [tr for tr in itertools.combinations(V, 3)]
atoms = [('E', p) for p in V] + [('T', p, 'u') for p in V] + [('T', p, 'v') for p in V] + [('J', p, q) for p, q in itertools.combinations(V, 2)] + [('J3',) + tr for tr in TR]
lits = [(s, a) for a in atoms for s in (1, -1)]
def lit_val(c, u, v, lit):
    s, a = lit
    if a[0] == 'E': x = c.E(c.i[a[1]], u, v)
    elif a[0] == 'T': x = c.Tl(c.i[a[1]], u if a[2] == 'u' else v)
    elif a[0] == 'J': x = c.J(c.i[a[1]], c.i[a[2]], u, v)
    else: x = c.J3s[a[1:]](u, v)
    return s * x
def fmt(cl):
    def f(lit):
        s, a = lit
        t = f"E({a[1]})" if a[0] == 'E' else (f"T({a[1]},{a[2]})" if a[0] == 'T' else (f"J({a[1]}{a[2]})" if a[0] == 'J' else f"J3({''.join(a[1:])})"))
        return t if s > 0 else '~' + t
    return ' | '.join(f(l) for l in cl)
def holds(H, hyps, goal):
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in V}; c.J3s = {}
        for tr in TR: c.J3s[tr] = make_J3(pool, cls, E, X, tuple(idx[p] for p in tr), tr)
        for cl in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append([lit_val(c, u, v, l) for l in cl])
        ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in goal: cls.append([-w_, -lit_val(c, u, v, l)])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
one = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','b')]
T1 = ((-1, ('J','a','b')), (-1, ('J3','b','c','x')), (1, ('J','b','c')))
def subsumed(cl, S):
    s = set(cl); return any(set(c2) <= s and len(c2) < len(cl) for c2 in S)
t0 = time.time(); S = []; n = 0
for k in range(1, K + 1):
    for cl in itertools.combinations(lits, k):
        if len({a for s, a in cl}) < k: continue
        if cl == T1 or subsumed(cl, S): continue
        n += 1
        if holds(one, [], cl): S.append(cl)
    print(f"  K={k}: {len(S)} valid so far ({n} tested, {time.time()-t0:.0f}s)", flush=True)
pickle.dump(S, open(f't1loc_m{m}_K{K}.pkl', 'wb'))
print(f"m={m}: T1 from the {len(S)} local clauses: {holds(one, S, T1)}", flush=True)
if holds(one, S, T1):
    cur = list(S)
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds(one, trial, T1): cur = trial
    print(f"minimal set ({len(cur)}):")
    for cl in cur: print('   ', fmt(cl))
    pickle.dump(cur, open(f't1loc_min_m{m}_K{K}.pkl', 'wb'))
