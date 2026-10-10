"""Negative/positive signatures (reduced two-auxiliary language of pathclose4b.py) from the embeddable census algebras
of order <= 9: every path p0~...~pn of distinct vertices and every pair (x, y) of elements outside the path, x != y.
Usage: python3 census_neg.py n  -> census_<n>.neg / .pos"""
import sys, json, itertools, numpy as np
sys.path.insert(0, '/home/claude/pa8w/n4')
from pathclose4b import atoms_for
n = int(sys.argv[1]); atoms = atoms_for(n)
E = '/home/claude/pa8w/embed/pa8/'
algs = []
for k in range(1, 8): algs += json.load(open(E + f'ord{k}.json'))
for f in ['post8.log', 'post9_0.log', 'post9_1.log', 'post9_3.log']:
    for line in open(E + f):
        d = json.loads(line)
        if d.get('embeds') is not None: algs.append(d['A'])
print(len(algs), "embeddable algebras", flush=True)
fneg = open(f'census_{n}.neg', 'wb'); fpos = open(f'census_{n}.pos', 'wb'); nneg = npos = 0
for T in algs:
    T = np.array(T); N = len(T); TH = T.T; ar = np.arange(N)      # TH[p][q] = theta_p(q)
    mt = (TH == ar[:, None]) & (TH.T == ar[None, :]); np.fill_diagonal(mt, False)
    adj = {p: np.nonzero(mt[p])[0] for p in range(N)}
    def paths(pre):
        if len(pre) == n + 1: yield pre; return
        for q in adj[pre[-1]]:
            if q not in pre: yield from paths(pre + [q])
    for p0 in range(N):
        for P in paths([p0]):
            keep = np.ones((N, N), bool)
            cols = []
            for at in atoms:
                if at[0] == 'ch': v = np.broadcast_to(np.bool_(mt[P[at[1]], P[at[2]]]), (N, N))
                elif at[0] in ('x', 'y'):
                    z, k = at[0], at[1]
                    if k == 'comm': w = TH[:, P[at[2]]] == TH[P[at[2]], :]
                    elif k == 'zle': w = TH[P[at[2]], :] == ar
                    elif k == 'sees': w = TH[:, P[at[2]]] == TH[:, P[at[3]]]
                    elif k == 'seen': w = TH[P[at[2]], :] == TH[P[at[3]], :]
                    v = np.broadcast_to(w[:, None] if z == 'x' else w[None, :], (N, N))
                else:
                    k = at[1]
                    if k == 'comm': v = TH == TH.T
                    elif k == 'xley': v = TH.T == ar[:, None]
                    elif k == 'ylex': v = TH == ar[:, None]
                    else:
                        i = P[at[2]]
                        if k == 'sees': v = TH[:, i][:, None] == TH[:, i][None, :]
                        else: v = TH[i, :][:, None] == TH[i, :][None, :]
                cols.append(v[keep])
            packed = np.unique(np.packbits(np.stack(cols, axis=1), axis=1), axis=0)
            if mt[P[0], P[-1]]: fpos.write(packed.tobytes()); npos += len(packed)
            else: fneg.write(packed.tobytes()); nneg += len(packed)
fneg.close(); fpos.close(); print("rows", nneg, npos)
