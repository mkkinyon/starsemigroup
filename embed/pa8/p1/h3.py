import pickle, numpy as np, sys
from collections import Counter
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
R = np.concatenate([pickle.load(open(f, 'rb')) for f in sys.argv[2:]])
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
fails = Counter(); ex = {}; cnt = Counter(); tot = 0
def check(name, cond, s):
    if not cond: fails[name] += 1; ex.setdefault(name, s)
for row in R:
    if len(set(row[:4])) < 4: continue
    a, c, b, d, x = [P[i] for i in row]; s = (a, c, b, d, x); tot += 1
    Tb = lambda p: [t for t, tr in top_blocks(p, n) if tr]; Nb = lambda p: [t for t, tr in top_blocks(p, n) if not tr]
    A, C, B, D = Tb(a), Tb(c), Tb(b), Tb(d); sx = supp(x, n)
    Gam = join_classes([a, c], n); Del = join_classes([c, b], n); Lam = join_classes([b, d], n)
    u = m(x, a); su = supp(u, n); U = [t for t, tr in top_blocks(u, n) if tr]; V = [t for t, tr in top_blocks(m(x, c), n) if tr]
    match = []
    for Ai in A:
        G = next(G for G in Gam if Ai <= G); Ci = next(Cj for Cj in C if Cj <= G)
        Dl = next(K for K in Del if Ci <= K); Bi = next(Bj for Bj in B if Bj <= Dl)
        L = next(K for K in Lam if Bi <= K); Di = next(Dj for Dj in D if Dj <= L)
        match.append((Ai, Ci, Bi, Di, G, Dl, L))
    LamB = {L: i for i, (_, _, _, _, _, _, L) in enumerate(match)}
    check('N(a)=N(b) blocks', set(Nb(a)) == set(Nb(b)), s)
    check('A_i ∩ C_i nonempty', all(Ai & Ci for (Ai, Ci, *_) in match), s)
    check('U_l is union of A and of B', all((Ul == frozenset().union(*[Ai for Ai in A if Ai <= Ul])) and (Ul == frozenset().union(*[Bi for Bi in B if Bi <= Ul])) for Ul in U), s)
    for Z in [t for t, tr in top_blocks(d, n)]:
        L = next(K for K in Lam if Z <= K)
        Ntil_type = any((Z & sx) and (Z & sx) <= N for N in Nb(c) if N <= sx)
        V_type = any((Z & sx) and (Z & sx) <= Vk for Vk in V)
        cnt[('d-block', 'Ntil-type' if Ntil_type else ('V-type' if V_type else ('outside supp x' if not (Z & sx) else 'other')), 'in Lambda_i' if L in LamB else 'free Lambda', 'T' if Z in D else 'N')] += 1
        if L in LamB:
            Ai = match[LamB[L]][0]
            check('T6: d-block in Lambda_i meets supp u only inside A_i', (Z & su) <= Ai, s)
            if Ntil_type: check('T5: Ntil-type d-block not in any Lambda_i', False, s)
print("instances:", tot)
for k, v in sorted(fails.items()): print(f"{v:5d} fail: {k}")
for k, v in sorted(cnt.items()): print(f"{v:6d} {k}")
pickle.dump(ex, open('h3_ex.pkl', 'wb'))
