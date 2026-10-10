"""Coarsen only the hub groups (merge A_G, C_G, B_G, D_G for hubs G); test hypotheses."""
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
for f in sys.argv[2:]:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a,c,b,d}) < 4: continue
    for u in us[:3]:
        s = structure(P, n, a, c, b, d, u, ys[0])
        hubs2 = [g for g in s.groups if g[3] in s.Nd and len(g[0]) >= 2]
        if not hubs2: continue
        keep = [i for i in range(len(s.match)) if not any(i in g[0] for g in hubs2)]
        at = [s.match[i][0] for i in keep] + [frozenset().union(*[s.match[i][0] for i in g[0]]) for g in hubs2]
        ct = [s.match[i][1] for i in keep] + [g[3] for g in hubs2]
        bt = [s.match[i][2] for i in keep] + [frozenset().union(*[s.match[i][2] for i in g[0]]) for g in hubs2]
        dt = [s.match[i][3] for i in keep] + [frozenset().union(*[s.match[i][3] for i in g[0]]) for g in hubs2]
        A2 = make(at, s.Na); C2 = make(ct, s.Nc); B2 = make(bt, s.Nb); D2 = make(dt, s.Nd)
        u0 = make([], s.Na + at)
        path_ok = bool(Mt[A2, C2] and Mt[C2, B2] and Mt[B2, D2]); u_ok = bool(th(C2, u0) == th(D2, u0))
        yok = [bool(comm[y, A2] and comm[y, B2] and th(y, C2) == th(y, B2)) for y in ys]
        k = ('path', path_ok, 'u', u_ok, 'some y', any(yok), 'a~d', bool(Mt[A2, D2])); stats[k] = stats.get(k, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
