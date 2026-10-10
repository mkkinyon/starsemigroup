"""Do the decoded identities suffice? search P_4 for a|><|c|><|b|><|d, u<=a, ud=ucbd, y~a, y~b, y.ad=y.acbd (and ycb=yb), not a|><|d."""
import pickle, numpy as np, sys, time
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
n = 4; P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None]); Mt = (T.T == ar[:, None]) & (T == ar[None, :])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def word(*idx):
    r = P[idx[0]]
    for i in idx[1:]: r = m(r, P[i])
    return r
t0 = time.time(); found = {}; np_ = 0
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                if Mt[a, d] or len({a, c, b, d}) < 4: continue
                np_ += 1
                us = [u for u in ar[le[ar, a]] if word(u, d) == word(u, c, b, d)]
                if not us: continue
                ys = ar[comm[ar, a] & comm[ar, b]]
                ad = word(a, d); acbd = word(a, c, b, d)
                for y in ys:
                    if m(P[y], ad) == m(P[y], acbd):
                        k2 = word(y, c, b) == word(y, b)
                        key = ('ycb=yb' if k2 else 'ycb!=yb')
                        found.setdefault(key, []).append((a, c, b, d, tuple(us), y))
print("non-closed distinct paths", np_, {k: len(v) for k, v in found.items()}, f"({time.time()-t0:.0f}s)")
pickle.dump(found, open('suff_found.pkl', 'wb'))
