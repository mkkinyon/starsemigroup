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
fails = Counter(); ex = {}; cnt = Counter()
def check(name, cond, s):
    if not cond: fails[name] += 1; ex.setdefault(name, s)
for row in R:
    if len(set(row[:4])) < 4: continue
    a, c, b, d, x = [P[i] for i in row]; s = (a, c, b, d, x)
    Tb = lambda p: [t for t, tr in top_blocks(p, n) if tr]; Nb = lambda p: [t for t, tr in top_blocks(p, n) if not tr]
    A, C, B, D = Tb(a), Tb(c), Tb(b), Tb(d); sx = supp(x, n); sa, sc, sb, sd = supp(a, n), supp(c, n), supp(b, n), supp(d, n)
    Gam = join_classes([a, c], n); Del = join_classes([c, b], n); Lam = join_classes([b, d], n); rho = join_classes([a, d], n)
    cbl = [t for t, tr in top_blocks(c, n)]; bbl = [t for t, tr in top_blocks(b, n)]; abl = [t for t, tr in top_blocks(a, n)]; dbl = [t for t, tr in top_blocks(d, n)]
    Dof = {E: next(K for K in Del if E <= K) for E in cbl + bbl}
    match = []
    for Ai in A:
        G = next(G for G in Gam if Ai <= G); Ci = next(Cj for Cj in C if Cj <= G)
        Dl = Dof[Ci]; Bi = next(Bj for Bj in B if Bj <= Dl)
        L = next(K for K in Lam if Bi <= K); Di = next(Dj for Dj in D if Dj <= L)
        match.append((Ai, Ci, Bi, Di, G, Dl, L))
    DeltaB = {Dl for (_,_,_,_,_,Dl,_) in match}
    def touched_by_a(Yb): return {Dof[E] for E in cbl if E & Yb}
    def touched_by_d(Z): return {Dof[E] for E in bbl if E & Z}
    for (Ai, Ci, Bi, Di, G, Dl, L) in match:
        tA = touched_by_a(Ai); tD = touched_by_d(Di)
        check('A_i touches no Delta_j (j≠i)', all(K == Dl or K not in DeltaB for K in tA), s)
        check('D_i touches no Delta_j (j≠i)', all(K == Dl or K not in DeltaB for K in tD), s)
        check('A_i touches no free Delta', all(K in DeltaB for K in tA), s)
        check('D_i touches no free Delta', all(K in DeltaB for K in tD), s)
        check('A_i meets C_i', bool(Ai & Ci), s); check('D_i meets B_i', bool(Di & Bi), s)
    for Yb in Nb(a):
        tA = touched_by_a(Yb); k = sum(1 for K in tA if K in DeltaB)
        check('N(a) touches ≤1 Delta_j', k <= 1, s)
        cnt[('N(a)', 'in supp x' if Yb <= sx else ('outside' if not (Yb & sx) else 'mixed'), f'DeltaB={k}', f'free={sum(1 for K in tA if K not in DeltaB)}')] += 1
    for Z in Nb(d):
        tD = touched_by_d(Z); k = sum(1 for K in tD if K in DeltaB)
        check('N(d) touches ≤1 Delta_j', k <= 1, s)
        cnt[('N(d)', 'in supp x' if Z <= sx else ('outside' if not (Z & sx) else 'mixed'), f'DeltaB={k}', f'free={sum(1 for K in tD if K not in DeltaB)}')] += 1
    # free Delta classes: which a-blocks / d-blocks touch them, and do they touch B-containing classes too?
    for K in Del:
        if K in DeltaB: continue
        ab_ = [Yb for Yb in abl if any(E & Yb for E in cbl if Dof[E] == K)]
        db_ = [Z for Z in dbl if any(E & Z for E in bbl if Dof[E] == K)]
        na = sum(1 for Yb in ab_ if any(Dof[E] in DeltaB for E in cbl if E & Yb))
        nd = sum(1 for Z in db_ if any(Dof[E] in DeltaB for E in bbl if E & Z))
        cnt[('free Delta', f'#a-blocks also touching some Delta_j={na}', f'#d-blocks also touching some Delta_j={nd}')] += 1
print("instances:", sum(1 for row in R if len(set(row[:4])) == 4))
for k, v in sorted(fails.items()): print(f"{v:5d} fail: {k}")
for k, v in sorted(cnt.items()): print(f"{v:6d} {k}")
pickle.dump(ex, open('h2_ex.pkl', 'wb'))
