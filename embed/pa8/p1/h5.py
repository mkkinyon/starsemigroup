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
fails = Counter(); ex = {}; tot = 0; cnt = Counter()
def check(name, cond, s):
    if not cond: fails[name] += 1; ex.setdefault(name, s)
for row in R:
    if len(set(row[:4])) < 4: continue
    a, c, b, d, x = [P[i] for i in row]; s = (a, c, b, d, x); tot += 1
    Tb = lambda p: [t for t, tr in top_blocks(p, n) if tr]; Nb = lambda p: [t for t, tr in top_blocks(p, n) if not tr]
    A, C, B, D = Tb(a), Tb(c), Tb(b), Tb(d); sx = supp(x, n); su = supp(m(x, a), n)
    Gam = join_classes([a, c], n); Del = join_classes([c, b], n); Lam = join_classes([b, d], n)
    dbl = [t for t, tr in top_blocks(d, n)]
    match = []
    for Ai in A:
        G = next(G for G in Gam if Ai <= G); Ci = next(Cj for Cj in C if Cj <= G)
        Dl = next(K for K in Del if Ci <= K); Bi = next(Bj for Bj in B if Bj <= Dl)
        L = next(K for K in Lam if Bi <= K); Di = next(Dj for Dj in D if Dj <= L)
        match.append((Ai, Ci, Bi, Di, G, Dl, L))
    for Nt in Nb(c):
        if not (Nt <= sx): continue
        G = next(G for G in Gam if Nt <= G); Dl = next(K for K in Del if Nt <= K)
        i_G = next((i for i, t in enumerate(match) if t[4] == G), None); i_D = next((i for i, t in enumerate(match) if t[5] == Dl), None)
        metsU = bool(Nt & su)
        metsLam = [i for i, t in enumerate(match) if any((Z & Nt) for Z in dbl if Z <= t[6])]
        cnt[('Ntil', 'meets U' if metsU else 'no U', f'Gamma has A={i_G is not None}', f'Delta has B={i_D is not None}', 'same index' if (i_G is not None and i_G == i_D) else '')] += 1
        if i_D is not None and metsU: check("T9'': Ntil in supp x meeting supp u, in Delta_s => in Gamma_s", i_G == i_D, s)
        if i_D is not None and i_D in metsLam: check("T9''': Ntil in Delta_s met by a d-block of Lambda_s => in Gamma_s", i_G == i_D, s)
        if i_G is not None: check("T10: Ntil in Gamma_r => in Delta_r", i_D == i_G, s)
print("instances:", tot)
for k, v in sorted(fails.items()): print(f"{v:5d} fail: {k}")
for k, v in sorted(cnt.items()): print(f"{v:6d} {k}")
pickle.dump(ex, open('h5_ex.pkl', 'wb'))
