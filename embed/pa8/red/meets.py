"""Meet statements (P) ^ (Q) = (R) for joins of eps_a, eps_b, eps_c, eps_y under (W_2), and hypothesis-dropping for T."""
import sys, time, itertools
exec(open('goal2.py').read().split("GOAL = ")[0])
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
def jatom(S):   # join of a set of letters -> atom
    S = tuple(sorted(S))
    if len(S) == 1: return ('E', S[0])
    if len(S) == 2: return ('J',) + S
    return ('J3',) + S
def meet(P, Q, R):   # (P)^(Q) <= (R):  ~J(P) | ~J(Q) | J(R)
    return ((-1, jatom(P)), (-1, jatom(Q)), (1, jatom(R)))
L = 'abcy'
subsets = [frozenset(s) for k in (1, 2, 3) for s in itertools.combinations(L, k)]
results = []
t0 = time.time()
for P in subsets:
    for Q in subsets:
        if P >= Q or Q >= P or P > Q: continue
        if sorted(P) > sorted(Q): continue
        R = P & Q
        if not R: continue       # meet <= empty partition: skip (would mean u = v)
        # test (P)^(Q) <= (R) with R = P∩Q  (the natural candidate; also R = any subset of P∩Q is weaker when smaller... larger R weaker)
        ok = holds2(W2, [], meet(P, Q, R))
        if ok: results.append((''.join(sorted(P)), ''.join(sorted(Q)), ''.join(sorted(R))))
print(f"m={m}: valid meets (P)^(Q) <= (P n Q) under (W_2) ({time.time()-t0:.0f}s):")
for r in results: print('   ', f"({r[0]}) ^ ({r[1]}) <= ({r[2]})")
# T and its hypothesis dependence
Tst = meet(frozenset('ab'), frozenset('bcy'), frozenset('bc'))
print(f"m={m}: T under (W_2): {holds2(W2, [], Tst)}")
for i, h in enumerate(W2):
    H = [x for j, x in enumerate(W2) if j != i]
    print(f"   T without {h}: {holds2(H, [], Tst)}")
