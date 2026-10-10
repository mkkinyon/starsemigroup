import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T)
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]
SUPP = [frozenset().union(*TB[i]) if TB[i] else frozenset() for i in range(N)]
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
def subgoals(a, d):
    cl = join_classes([P[a], P[d]], n)
    g1a = all(sum(1 for A in TB[a] if A <= K) <= 1 for K in cl)
    g1b = all(any(K & SUPP[d]) for K in cl if any(A <= K for A in TB[a]))
    return g1a, g1b
drop = int(sys.argv[1]); want1a = sys.argv[2] == 'T'; shown = 0
paths = [(a, c, b, d) for a in range(N) for c in nb[a] for b in nb[c] for d in nb[b]]
for a, c, b, d in paths:
    if Mt[a, d] or len({a,b,c,d}) < 4: continue
    g1a, g1b = subgoals(a, d)
    if g1a != want1a: continue
    hx = [comm[ar, a], th(c, ar) == th(d, ar)]
    hy = [comm[ar, a], comm[ar, b], th(ar, c) == th(ar, b)]
    ex = [h for i, h in enumerate(hx) if i != drop]; ey = [h for i, h in enumerate(hy) if i + 2 != drop]
    okx = np.logical_and.reduce(ex) if ex else np.ones(N, bool); oky = np.logical_and.reduce(ey) if ey else np.ones(N, bool)
    if okx.any() and oky.any():
        # prefer witnesses of maximal rank
        xs = ar[okx]; ys = ar[oky]
        x = max(xs, key=lambda i: len(TB[i])); y = max(ys, key=lambda i: len(TB[i]))
        print("--- 1a", g1a, "1b", g1b)
        for nm, i in zip('acbdxy', (a, c, b, d, x, y)): print(f"  {nm} = {show(i)}")
        print("  rho:", [sorted(K) for K in join_classes([P[a], P[d]], n)])
        shown += 1
        if shown >= int(sys.argv[3]): break
