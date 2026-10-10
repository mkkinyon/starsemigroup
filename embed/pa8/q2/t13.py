"""Test (T1),(T2) on u-only instances in P_4 (all) : does the u-hypothesis alone give them?"""
import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from hq import structure, cls, show
from t12 import kappas
n = 4; P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); Mt = (T.T == ar[:, None]) & (T == ar[None, :]); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
y0 = next(i for i in range(N) if len(P[i]) == 2 and len(list(P[i])[0]) == n)  # rank-0 one block (only as placeholder)
stats = {}; ex = {}
for a in range(N):
  for c in nb[a]:
    for b in nb[c]:
      for d in nb[b]:
        if len({a,c,b,d}) < 4: continue
        us = ar[le[ar, a] & (th(c, ar) == th(d, ar))]
        hy = (comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))).any()
        for u in us:
            s = structure(P, n, a, c, b, d, u, y0)
            for (idx, lab, AG, CG) in s.groups:
                if not lab: continue
                GG = cls(CG, s.Pi1)
                for kap in kappas(s, GG):
                    alpha = [i for i in idx if any(E & s.match[i][0] for E in kap if E in s.Nc)]
                    Ds = [k for k in idx if any(F & s.match[k][3] for F in kap if F in s.Na)]
                    T1 = len(Ds) <= 1; T2 = not (alpha and Ds and alpha != Ds)
                    key = ('y' if hy else 'noy', 'ab=ba' if comm[a, b] else 'ab!=ba', 'T1', T1, 'T2', T2)
                    stats[key] = stats.get(key, 0) + 1
                    if key not in ex: ex[key] = (a, c, b, d, u, idx)
for k in sorted(stats): print(stats[k], k)
