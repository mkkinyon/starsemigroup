"""For the order-9 candidates with length-4 paths (cand 1, 3): which (x,y)-rows (signatures over the 78-atom language) are NOT
contained in any negative record of the P_5 sample?  Such rows are the only possible explanations by a 2-aux length-4 condition."""
import sys, json, itertools, numpy as np, time
sys.path.insert(0, '/home/claude/pa8w/n4')
from pathclose4b import atoms_for, fmt
n = 4; atoms = atoms_for(n); nat = len(atoms); RB = (nat + 7) // 8
C9 = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))
neg = np.fromfile('all_5_4.neg', dtype=np.uint8).reshape(-1, RB)
print("negative records", len(neg), flush=True)
negu = np.unique(neg, axis=0); print("unique", len(negu), flush=True)
def rows_for(T):
    T = np.array(T); N = len(T); TH = T.T; ar = np.arange(N)
    mt = (TH == ar[:, None]) & (TH.T == ar[None, :]); np.fill_diagonal(mt, False)
    out = []
    for P in itertools.permutations(range(N), n + 1):
        if not all(mt[P[i], P[i+1]] for i in range(n)) or mt[P[0], P[-1]] or P[0] > P[-1]: continue
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
                    v = TH[:, i][:, None] == TH[:, i][None, :] if k == 'sees' else TH[i, :][:, None] == TH[i, :][None, :]
            cols.append(v.reshape(-1))
        M = np.stack(cols, axis=1)
        for xy in range(N * N): out.append((P, xy // N, xy % N, M[xy]))
    return out
for c in (1, 3):
    rows = rows_for(C9[c]); print(f"cand {c}: {len(rows)} (path,x,y) rows", flush=True)
    unexplained = 0
    for P, x, y, r in rows:
        rp = np.packbits(r)
        # contained in some negative record?  (r & ~s) == 0
        cont = ((rp[None, :] & ~negu) == 0).all(axis=1).any()
        if not cont:
            unexplained += 1
            print("  NOT covered:", P, x, y, [fmt(atoms[k]) for k in np.nonzero(r)[0]], flush=True)
    print(f"cand {c}: {unexplained} rows not covered by a P_5 negative record", flush=True)
