"""Random-path verification in P(P_m) of two-auxiliary candidates.  Usage: python3 pathclose2r.py m n cands.json secs"""
import sys, json, time, random, numpy as np
from pa_embed2 import PPm
from pathclose2 import fmt2
m = int(sys.argv[1]); n = int(sys.argv[2]); combos = [tuple(tuple(a) for a in c) for c in json.load(open(sys.argv[3]))]; secs = float(sys.argv[4])
D = PPm(m); N = D.N; TH = np.array(D.tab).T; ar = np.arange(N)
mt = (TH == ar[:, None]) & (TH.T == ar[None, :]); matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
V = ['p%d' % i for i in range(n + 1)]
commXY = TH == TH.T; xleY = (TH.T == ar[:, None]); ylex = (TH == ar[:, None])
def atom_mat(at, P):
    if at[0] in ('x', 'y'):
        z, k = at[0], at[1]
        if k == 'comm': v = TH[:, P[at[2]]] == TH[P[at[2]], :]
        elif k == 'zle': v = TH[P[at[2]], :] == ar
        elif k == 'lez': v = TH[:, P[at[2]]] == P[at[2]]
        elif k == 'sees': v = TH[:, P[at[2]]] == TH[:, P[at[3]]]
        elif k == 'seen': v = TH[P[at[2]], :] == TH[P[at[3]], :]
        elif k == 'zeq': v = TH[P[at[2]], P[at[3]]] == ar
        return v[:, None] if z == 'x' else v[None, :]
    k = at[1]
    if k == 'comm': return commXY
    if k == 'xley': return xleY
    if k == 'ylex': return ylex
    i = P[at[2]]
    if k == 'sees': return TH[:, i][:, None] == TH[:, i][None, :]
    if k == 'seen': return TH[i, :][:, None] == TH[i, :][None, :]
    if k == 'x=th_y': return TH[:, i][None, :] == ar[:, None]
    if k == 'y=th_x': return TH[:, i][:, None] == ar[None, :]
    if k == 'x=th_p_y': return TH[i, :][None, :] == ar[:, None]
    if k == 'y=th_p_x': return TH[i, :][:, None] == ar[None, :]
alive = list(combos); refuted = {}; t0 = time.time(); npaths = 0
while time.time() - t0 < secs and alive:
    P = [random.randrange(N)]
    for _ in range(n): P.append(random.choice(matched[P[-1]]))
    if len(set(P)) < len(P) or mt[P[0], P[-1]]: continue
    npaths += 1
    keep = np.ones((N, N), bool); keep[list(P), :] = False; keep[:, list(P)] = False; np.fill_diagonal(keep, False)
    cache = {}; still = []
    for c in alive:
        v = keep.copy()
        for at in c:
            if at not in cache: cache[at] = atom_mat(at, P)
            v &= cache[at]
            if not v.any(): break
        if v.any(): refuted[c] = (P, [int(t) for t in np.argwhere(v)[0]])
        else: still.append(c)
    alive = still
print(f"m={m}, n={n}: {npaths} random open paths in {secs}s; refuted {len(refuted)}:")
for c, w in refuted.items(): print("  ", [fmt2(at, V) for at in c], w)
print("survivors:", len(alive))
json.dump([[list(a) for a in c] for c in alive], open(sys.argv[3].replace('.json', '_surv.json'), 'w'))
