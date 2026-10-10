import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])   # le[q,p]: q<=p
Mt = (T.T == ar[:, None]) & (T == ar[None, :])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]
NB = [[t for t, tr in top_blocks(P[i], n) if not tr] for i in range(N)]
SUPP = [frozenset().union(*TB[i]) if TB[i] else frozenset() for i in range(N)]
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
def Yc(a, b, c):
    ok = all((A & SUPP[c]) <= SUPP[b] or not (A & SUPP[b]) for A in TB[a])
    ok2 = all((F & SUPP[c]) <= SUPP[b] or F in NB[b] or all(any(F == frozenset().union(*S) for S in [()]) for _ in [0]) or F <= SUPP[b] and all(B <= F or not (B & F) for B in TB[b]) for F in NB[a])
    return ok, ok2
paths = [(a, c, b, d) for a in range(N) for c in nb[a] for b in nb[c] for d in nb[b]]
bad = []; cnt = 0
for a, c, b, d in paths:
    if Mt[a, d]: continue
    hx = comm[ar, a] & (th(c, ar) == th(d, ar))
    if not hx.any(): continue
    hy = comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))
    assert not hy.any()
    ok, ok2 = Yc(a, b, c)
    if ok and ok2:
        cnt += 1
        if len(bad) < 4 and len({a, b, c, d}) == 4:
            bad.append((a, c, b, d))
print("non-closed paths with x-witness and (Yc),(Yc') satisfied:", cnt)
for a, c, b, d in bad:
    print('---')
    for nm, i in zip('acbd', (a, c, b, d)): print(f"  {nm} = {show(i)}")
    xs = ar[comm[ar, a] & (th(c, ar) == th(d, ar)) & le[ar, a]]
    print("  u in:", '; '.join(show(i) for i in xs))
