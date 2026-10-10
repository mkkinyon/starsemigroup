"""Experiments on the structure of instances of (V) in P(P_m)."""
import sys, itertools; sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pa_embed2 import PPm
import numpy as np
m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
D = PPm(m); N = D.N; TH = np.array(D.tab).T; ar = np.arange(N); le = (TH.T == ar[:, None]); fix = (TH == ar[:, None])
def blocks(p):
    out = []
    for blk in D.projs[p]:
        up = frozenset(i for i in blk if i < m)
        if up: out.append((up, any(i >= m for i in blk)))
    return out
BL = [blocks(p) for p in range(N)]
def supp(p): return frozenset().union(*[b for b, tr in BL[p] if tr]) if any(tr for b, tr in BL[p]) else frozenset()
def Tb(p): return [b for b, tr in BL[p] if tr]
def Nb(p): return [b for b, tr in BL[p] if not tr]
def join(p, q):
    """classes of eps_p v eps_q"""
    par = list(range(m))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for r in (p, q):
        for b, _ in BL[r]:
            b = list(b)
            for i in b[1:]: par[f(i)] = f(b[0])
    cl = {}
    for i in range(m): cl.setdefault(f(i), set()).add(i)
    return [frozenset(c) for c in cl.values()]
def instances():
    for a in range(N):
        for c in range(N):
            for t in range(N):
                w = TH[c, t]
                if not le[w, a]: continue
                z = TH[a, t]
                for b in range(N):
                    if fix[b, c] and le[z, b]: yield a, b, c, t, z, w, TH[b, t]
if __name__ == "__main__":
    from collections import Counter
    cnt = Counter(); n = 0
    for a, b, c, t, z, w, s in instances():
        n += 1
        SA, SB, SC = supp(a), supp(b), supp(c)
        cnt['Tb in supp a'] += all(B <= SA for B in Tb(b))
        cnt['Ta in supp b'] += all(A <= SB for A in Tb(a))
        cnt['supp a = supp b'] += SA == SB
        cnt['Ja = Jb'] += set(join(a, t)) == set(join(b, t))
        cnt['N(a)=N(b)'] += set(Nb(a)) == set(Nb(b))
        cnt['eps_a = eps_b'] += set(b_ for b_, _ in BL[a]) == set(b_ for b_, _ in BL[b])
        cnt['Tc in supp a'] += all(C <= SA for C in Tb(c))
        cnt['Ta in supp c'] += all(A <= SC for A in Tb(a))
        cnt['Tb in supp c'] += all(B <= SC for B in Tb(b))
        cnt['supp c = supp a'] += SA == SC
    print(n, "instances"); 
    for k, v in cnt.items(): print(f"  {k}: {v}")
