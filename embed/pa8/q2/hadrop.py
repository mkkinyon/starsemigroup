import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]; comm = (T == T.T); Mt = (T.T == ar[:, None]) & (T == ar[None, :]); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]; NB = [[t for t, tr in top_blocks(P[i], n) if not tr] for i in range(N)]
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
res = {}; ex = {}
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                if len({a,c,b,d}) < 4: continue
                hx = (le[ar, a] & (th(c, ar) == th(d, ar))).any(); hy = (comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))).any()
                Hd = all(sum(1 for A in TB[a] if A & E) <= 1 for E in NB[d])
                k = (hx, hy, Hd); res[k] = res.get(k, 0) + 1
                if k not in ex: ex[k] = (a, c, b, d)
for k in sorted(res): print("u", k[0], "y", k[1], "Hd", k[2], ":", res[k])
for k in [(True, False, False), (False, True, False)]:
    if k in ex:
        a, c, b, d = ex[k]; print('---', k)
        for nm, i in zip('acbd', (a, c, b, d)): print(f"  {nm} = {show(i)}")
        if k[0]: print("  u in:", '; '.join(show(i) for i in ar[le[ar, a] & (th(c, ar) == th(d, ar))]))
        if k[1]: print("  y in:", '; '.join(show(i) for i in ar[comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))]))
