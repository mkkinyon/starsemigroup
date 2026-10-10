"""Path-closing search directly in P(P_m) with numpy signatures.  Usage: python3 pathclose_np.py m n maxsize"""
import sys, json, itertools, numpy as np
from pa_embed2 import PPm
from pathclose import fmt
def run(m, n, maxsize):
    D = PPm(m); N = D.N; tab = np.array(D.tab); TH = tab.T; ar = np.arange(N)
    mt = (TH == ar[:, None]) & (TH.T == ar[None, :])
    matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
    V = ['p%d' % i for i in range(n + 1)]
    atoms = []
    for i in range(n + 1): atoms += [('comm', i), ('xle', i), ('lex', i)]
    for i, j in itertools.combinations(range(n + 1), 2): atoms += [('sees', i, j), ('seen', i, j)]
    for i in range(n + 1):
        for j in range(n + 1):
            if i != j: atoms.append(('xeq', i, j))
    def atomvec(at, P):
        k = at[0]
        if k == 'comm': return TH[:, P[at[1]]] == TH[P[at[1]], :]
        if k == 'xle': return TH[P[at[1]], :] == ar
        if k == 'lex': return TH[:, P[at[1]]] == P[at[1]]
        if k == 'sees': return TH[:, P[at[1]]] == TH[:, P[at[2]]]
        if k == 'seen': return TH[P[at[1]], :] == TH[P[at[2]], :]
        if k == 'xeq': return TH[P[at[1]], P[at[2]]] == ar
    def paths(prefix):
        if len(prefix) == n + 1:
            yield prefix; return
        for q in matched[prefix[-1]]:
            yield from paths(prefix + [q])
    neg = set(); pos = set(); npaths = 0
    weights = np.array([1 << k for k in range(len(atoms))], dtype=object)
    for p0 in range(N):
        for P in paths([p0]):
            if len(set(P)) < len(P): continue
            npaths += 1
            M = np.stack([atomvec(at, P) for at in atoms], axis=1)   # N x natoms
            M[list(P), :] = False
            keep = np.ones(N, bool); keep[list(P)] = False
            sigs = {int(sum(int(b) << k for k, b in enumerate(row))) for row in M[keep]}
            (pos if mt[P[0], P[-1]] else neg).update(sigs)
    negl = sorted(neg, key=lambda s: -bin(s).count('1')); maxs = []
    for s in negl:
        if not any((s & t) == s for t in maxs): maxs.append(s)
    print(f"m={m}, n={n}: {npaths} paths, {len(neg)} negative signatures, {len(maxs)} maximal, {len(pos)} positive", flush=True)
    out = []
    for size in range(1, maxsize + 1):
        for combo in itertools.combinations(range(len(atoms)), size):
            H = sum(1 << k for k in combo)
            if any((H & s) == H for s in maxs): continue
            if any((h & H) == h for h in out): continue
            if not any((H & s) == H for s in pos): continue
            out.append(H); print("  ", size, [fmt(atoms[k], V) for k in combo], flush=True)
    json.dump([[list(atoms[k]) for k in range(len(atoms)) if H >> k & 1] for H in out], open(f"pc_np_{m}_{n}.json", "w"))
    return out
if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
