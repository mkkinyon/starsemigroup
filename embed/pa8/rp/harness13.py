import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
from pmon import canon
fails = {}; ex = {}; count = 0
def matched(p, q): return th(p, q) == p and th(q, p) == q
def comm(p, q): return m(p, q) == m(q, p)
def hyps(a, c, b, x, y): return matched(a, c) and matched(b, c) and comm(x, c) and th(x, a) == th(x, c) and comm(y, a) and th(x, b) == th(y, b)
def make_T(p, blocks_to_T):
    # projection p (pmon format) with the given top N-blocks made transversal
    res = []
    used = set()
    for blk in p:
        top = frozenset(i for i in blk if i < n)
        if top in blocks_to_T and all(i < n for i in blk):
            res.append(sorted(top) + [n + i for i in sorted(top)]); used.add(top)
        elif (not any(i < n for i in blk)) and frozenset(i - n for i in blk) in blocks_to_T:
            continue
        else: res.append(list(blk))
    return canon(res)
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    # reduction (ii): N(y)-blocks inside supp a made transversal in x and y
    Ms = {N for N in s.Ny if N <= s.sa}
    if Ms:
        x2 = make_T(x, Ms); y2 = make_T(y, Ms)
        check('Red2: modified (x,y) still satisfies the hypotheses', hyps(a, c, b, x2, y2), fails, ex, s)
        check('Red2b: x2 <= y2', th(y2, x2) == x2, fails, ex, s)
    # L2: every c-block inside one class of x∨a; K_N has no A and trace N
    xa = s.kappa  # placeholder
    Kx = join_classes([x, a], n)
    for E in [t for t, tr in top_blocks(c, n)]:
        check('L2a: c-block inside one x∨a class', sum(1 for K in Kx if E & K) == 1, fails, ex, s)
    for N in s.Nc:
        if N <= s.sx:
            K = next(K for K in Kx if N <= K)
            check('L2b: K_N ∩ supp x = N', (K & s.sx) == N, fails, ex, s)
            check('L2c: K_N has no A', not any(A <= K for A in s.A), fails, ex, s)
            G = next(G for G in s.Gamma if N <= G)
            check('L2d: Gamma(N) ⊆ K_N', G <= K, fails, ex, s)
            cb = [E for E in [t for t, tr in top_blocks(c, n)] if E <= G]
            check('L2e: c-blocks of Gamma(N) are N and Ntil-blocks', all(E == N or E in s.Ntil for E in cb), fails, ex, s)
    for N in s.Ntil:
        F = next(D for D in s.Delta if N <= D)
        check('L1a: Delta(Ntil) ∩ supp y = Ntil', (F & s.sy) == N, fails, ex, s)
        check('L1b: Delta(Ntil) has no B', not any(B <= F for B in s.B), fails, ex, s)
    for (Ai, Ci, Bi, G, Dl) in s.match:
        cb = [E for E in [t for t, tr in top_blocks(c, n)] if E <= G]
        check('L3: c-blocks of Gamma_i are C_i and Ntil-blocks', all(E == Ci or E in s.Ntil for E in cb), fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness13_ex.pkl', 'wb'))
