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
        if all(len(g[0]) == 1 for g in s.groups): continue
        at = [frozenset().union(*[s.match[i][0] for i in g[0]]) for g in s.groups]; ct = [frozenset().union(*[s.match[i][1] for i in g[0]]) for g in s.groups]
        bt = [frozenset().union(*[s.match[i][2] for i in g[0]]) for g in s.groups]; dt = [frozenset().union(*[s.match[i][3] for i in g[0]]) for g in s.groups]
        A2 = make(at, s.Na); C2 = make(ct, s.Nc); B2 = make(bt, s.Nb); D2 = make(dt, s.Nd)
        u0 = make([], s.Na + at)
        path_ok = bool(Mt[A2, C2] and Mt[C2, B2] and Mt[B2, D2]); u_ok = bool(th(C2, u0) == th(D2, u0))
        yok = [bool(comm[y, A2] and comm[y, B2] and th(y, C2) == th(y, B2)) for y in ys]
        concl = bool(Mt[A2, D2])
        k = ('path', path_ok, 'u', u_ok, 'some y', any(yok), 'all y', all(yok), 'a~d~', concl); stats[k] = stats.get(k, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
