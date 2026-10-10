import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from hq import structure, cls
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
idx = {frozenset(frozenset(b) for b in p): i for i, p in enumerate(P)}
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None]); Mt = (T.T == ar[:, None]) & (T == ar[None, :])
def make(tblocks, nblocks):
    blocks = [t | frozenset(j + n for j in t) for t in tblocks]
    for t in nblocks: blocks.append(t); blocks.append(frozenset(j + n for j in t))
    return idx[frozenset(blocks)]
stats = {}
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    for u in us:
        s = structure(P, n, a, c, b, d, u, ys[0])
        hubs = [g for g in s.groups if g[3] in s.Nd]; nonhubs = [g for g in s.groups if g[3] not in s.Nd]
        if not hubs or not nonhubs: continue
        tb = [s.match[k][3] for g in nonhubs for k in g[0]] + [s.match[i][1] for g in hubs for i in g[0]]
        d1 = make(tb, s.Nc)
        k1 = ('step1 (a,c,b,d1):', 'b~d1', bool(Mt[b, d1]), 'u', bool(th(c, u) == th(d1, u)), 'y', any(th(y, c) == th(y, b) for y in ys), 'a~d1', bool(Mt[a, d1]))
        k2 = ('step2 (a,d1,b,d):', 'u', bool(th(d1, u) == th(d, u)), 'y', any(th(y, d1) == th(y, b) and comm[y, a] and comm[y, b] for y in ys))
        stats[k1] = stats.get(k1, 0) + 1; stats[k2] = stats.get(k2, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
