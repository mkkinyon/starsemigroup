import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]          # theta_x(p)
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T)
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]
SUPP = [frozenset().union(*TB[i]) if TB[i] else frozenset() for i in range(N)]
def subgoals(a, d):
    cl = join_classes([P[a], P[d]], n)
    g1a = all(sum(1 for A in TB[a] if A <= K) <= 1 for K in cl)
    g1b = all(any(K & SUPP[d]) for K in cl if any(A <= K for A in TB[a]))
    g2a = all(sum(1 for D in TB[d] if D <= K) <= 1 for K in cl)
    g2b = all(any(K & SUPP[a]) for K in cl if any(D <= K for D in TB[d]))
    return g1a, g1b, g2a, g2b
paths = [(a, c, b, d) for a in range(N) for c in nb[a] for b in nb[c] for d in nb[b]]
res = {}
for a, c, b, d in paths:
    if Mt[a, d]: continue
    sg = subgoals(a, d)
    hx = [comm[ar, a], th(c, ar) == th(d, ar)]
    hy = [comm[ar, a], comm[ar, b], th(ar, c) == th(ar, b)]
    for drop in range(5):
        ex = [h for i, h in enumerate(hx) if i != drop]; ey = [h for i, h in enumerate(hy) if i + 2 != drop]
        okx = np.logical_and.reduce(ex) if ex else np.ones(N, bool); oky = np.logical_and.reduce(ey) if ey else np.ones(N, bool)
        if okx.any() and oky.any():
            k = (drop, sg); res[k] = res.get(k, 0) + 1
names = ['drop xa=ax', 'drop th_c(x)=th_d(x)', 'drop ya=ay', 'drop yb=by', 'drop th_y(c)=th_y(b)']
print("subgoals: (1a) no two T(a) in a rho-class, (1b) T(a)-class meets supp d, (2a), (2b) dually")
for k in sorted(res): print(f"{names[k[0]]:22s} 1a {k[1][0]!s:5} 1b {k[1][1]!s:5} 2a {k[1][2]!s:5} 2b {k[1][3]!s:5}  paths: {res[k]}")
