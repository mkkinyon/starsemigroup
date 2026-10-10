import pickle, numpy as np, itertools, sys, time
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
rows = []
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                xs = ar[comm[ar, a] & comm[ar, c] & (th(a, ar) == th(b, ar)) & (th(ar, c) == th(ar, d))]
                for x in xs: rows.append((a, c, b, d, x))
R = np.array(rows); a, c, b, d, x = R.T
print("instances", len(R), "closed", Mt[a, d].all(), "distinct path", np.sum((a != b) & (c != d) & (a != d)))
pickle.dump(R, open('instP4.pkl', 'wb'))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbdx'
words = [w for l in (1, 2, 3) for w in itertools.product(L, repeat=l)]
def ev(w, I):
    dd = dict(zip(L, I)); r = dd[w[0]]
    for ch in w[1:]: r = m(r, dd[ch])
    return r
part = [words]
for row in R:
    I = [P[i] for i in row]; newpart = []
    for g in part:
        if len(g) == 1: newpart.append(g); continue
        dd = {}
        for w in g: dd.setdefault(ev(w, I), []).append(w)
        newpart.extend(dd.values())
    part = newpart
for g in sorted((g for g in part if len(g) > 1), key=lambda g: (min(len(w) for w in g), g)):
    print(' = '.join(''.join(w) for w in sorted(g, key=lambda w: (len(w), w))))
for l, r in [('ad','acbd'), ('xad','xacbd'), ('ad','acd'), ('ad','abd'), ('xad','xacd'), ('xad','xabd'), ('xd','xcd'), ('xd','xcbd'), ('xbd','xcbd'), ('bxd','bxcd'), ('uad?', '')]:
    if r: print(f"{l} = {r}: fails", sum(1 for row in R if ev(l, [P[i] for i in row]) != ev(r, [P[i] for i in row])))
