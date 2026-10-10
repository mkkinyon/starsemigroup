"""Clauses with exactly one J3 atom (over (a,b,c),(a,c,y),(b,c,y),(a,b,y)) and <= 3 further literals over (y,a,c,b), valid under (W_2).  Usage: python3 inv6.py m"""
import sys, time, itertools, pickle
sys.argv = [sys.argv[0], sys.argv[1], '3']
exec(open('goal2.py').read().split("GOAL = ")[0])
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb'))
TRIPLES = [('a','b','c'), ('a','c','y'), ('b','c','y'), ('a','b','y')]
def holds2(H, hyps, goal):
    T, idx = table(H, ('mt','a','b'))
    def extra(pool, E, Tl, J, cls, X):
        c = mkctx(pool, cls, E, Tl, J, X, idx, TRIPLES)
        for cl in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append(J3lits(c, u, v, cl))
        ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in J3lits(c, u, v, goal): cls.append([-w_, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
def fmt2(cl):
    def f(lit):
        s, a = lit
        if a[0] == 'J3': t = f"J3({''.join(a[1:])})"
        else: t = f"E({a[1]})" if a[0] == 'E' else (f"T({a[1]},{a[2]})" if a[0] == 'T' else f"J({a[1]}{a[2]})")
        return t if s > 0 else '~' + t
    return ' | '.join(f(l) for l in cl)
base_lits = lits
cands = []
for tr in TRIPLES:
    for s3 in (1, -1):
        j3 = (s3, ('J3',) + tr)
        for k in range(0, 3):
            for rest in itertools.combinations(base_lits, k):
                if len({a for s, a in rest}) < k: continue
                cands.append((j3,) + rest)
print(len(cands), 'candidate clauses', flush=True)
def subsumed(cl, Sset):
    s = set(cl); return any(set(c2) <= s and len(c2) < len(cl) for c2 in Sset)
# clauses already implied trivially: skip those whose non-J3 part is already a valid clause (in S)
Sset = set(S)
t0 = time.time(); V3 = []; n = 0
for cl in cands:
    rest = cl[1:]
    if subsumed(rest, Sset) or rest in Sset: continue
    if subsumed(cl, V3): continue
    n += 1
    if holds2(W2, [], cl): V3.append(cl)
print(f"m={m}: {len(V3)} minimal valid J3-clauses ({n} tested, {time.time()-t0:.0f}s)", flush=True)
for cl in V3: print('   ', fmt2(cl))
pickle.dump(V3, open(f'inv6_m{m}.pkl', 'wb'))
# minimise for GOAL
GOAL = ((-1, ('J3', 'a', 'b', 'c')), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('E','c')))
pool_ = S + [cl for cl in V3 if cl != GOAL]
if holds2(weak, pool_, GOAL):
    cur = list(pool_)
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds2(weak, trial, GOAL): cur = trial
    print(f"m={m}: GOAL follows from weak + {len(cur)} clauses:", flush=True)
    for cl in cur: print('   ', fmt2(cl))
else: print(f"m={m}: GOAL does not follow from weak + all local + J3 clauses", flush=True)
