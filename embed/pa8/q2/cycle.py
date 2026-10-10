"""Undo one pi-cycle of hub swaps: d2 := d with, for hubs G in the cycle, C_i (i in G) as T-blocks and E'_G as N-block. Test hypotheses."""
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
        hubs = [g for g in s.groups if g[3] in s.Nd]
        if len(hubs) < 2: continue
        # pi: hub G -> hub G' with D_{G'} = Gamma_G ∩ supp d
        def Dset(g): return frozenset().union(*[s.match[i][3] for i in g[0]])
        pi = {}
        for g in hubs:
            E = cls(g[3], s.Pi1) & s.sd
            tgt = [h for h in hubs if Dset(h) == E]
            if len(tgt) != 1: pi = None; break
            pi[g[0]] = tgt[0][0]
        if pi is None: stats['pi undefined'] = stats.get('pi undefined', 0) + 1; continue
        # cycles
        seen = set(); cycles = []
        for g in hubs:
            if g[0] in seen: continue
            cyc = []; x = g[0]
            while x not in seen: seen.add(x); cyc.append(x); x = pi[x]
            cycles.append(cyc)
        if len(cycles) < 2: stats['single cycle'] = stats.get('single cycle', 0) + 1; continue
        cyc = cycles[0]
        # build d2
        tb = [D for D in s.D]; nb = list(s.Nd)
        for gidx in cyc:
            g = next(h for h in hubs if h[0] == gidx)
            Ds = [s.match[k][3] for k in gidx]
            tb = [D for D in tb if D not in Ds] + [s.match[i][1] for i in gidx]
            nb = [E for E in nb if E != g[3]] + [Dset(g)]
        d2 = make(tb, nb)
        k = ('b~d2', bool(Mt[b, d2]), 'u', bool(th(c, u) == th(d2, u)), 'y', any(th(y, d2) == th(y, b) for y in ys), 'a~d2', bool(Mt[a, d2]),
             'step2 u', bool(th(d2, u) == th(d, u)), 'ncycles', len(cycles), 'sizes', tuple(sorted(len(g) for g in cyc)))
        stats[k] = stats.get(k, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
