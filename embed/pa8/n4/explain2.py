"""For each order-9 candidate: unclosed 2-paths (a,c,b); all (x,y) rows in the 45-atom language; rows not covered by the
P_5 negatives (pc4_5_2_4.neg) are greedily minimised under SAT validity at m=4 (then checked at m=5).
Usage: python3 explain2.py cand [cand ...]"""
import sys, os, json, itertools, numpy as np, time
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.insert(0, '/home/claude/pa8w/embed/pa8'); sys.path.insert(0, '/home/claude/pa8w/n4')
from pc3_verify import valid
from pathclose4b import atoms_for, fmt
n = 2; atoms = atoms_for(n); nat = len(atoms); RB = (nat + 7) // 8
C9 = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))
negu = np.unique(np.fromfile('/home/claude/pa8w/n4/pc4_5_2_4.neg', dtype=np.uint8).reshape(-1, RB), axis=0)
print("negative records (unique)", len(negu), flush=True)
def covered(S):
    r = np.zeros(nat, bool); r[list(S)] = True; rp = np.packbits(r)
    return bool(((rp[None, :] & ~negu) == 0).all(axis=1).any())
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
                    if k == 'sees': v = TH[:, i][:, None] == TH[:, i][None, :]
                    elif k == 'seen': v = TH[i, :][:, None] == TH[i, :][None, :]
                    else:
                        j = P[at[3]]
                        v = TH[:, i][:, None] == TH[:, j][None, :] if k == 'xsees' else TH[i, :][:, None] == TH[j, :][None, :]
            cols.append(v.reshape(-1))
        M = np.stack(cols, axis=1)
        for xy in range(N * N): out.append((P, xy // N, xy % N, M[xy]))
    return out
for c in map(int, sys.argv[1:]):
    rows = rows_for(C9[c]); print(f"=== cand {c}: {len(rows)} (path,x,y) rows", flush=True)
    found = {}
    for P, x, y, r in rows:
        S = list(np.nonzero(r)[0])
        if covered(S): continue
        # greedy minimisation under SAT m=4, trying to drop 'xy' and 'ch' atoms first, then zle/comm, then sees/seen
        order = sorted(S, key=lambda k: (0 if atoms[k][0] in ('xy', 'ch') else 1 if atoms[k][1] in ('zle', 'comm') else 2, k))
        try:
            for k in order:
                S2 = [j for j in S if j != k]
                if valid([atoms[j] for j in S2], n, 4): S = S2
        except ValueError: continue
        key = tuple(sorted(S))
        if key in found: continue
        H = [atoms[j] for j in S]
        try: v5 = valid(H, n, 5)
        except ValueError: v5 = 'err'
        found[key] = v5
        print(f"  path {P} x={x} y={y}: size {len(S)} valid m=5: {v5}\n     ", ', '.join(fmt(a) for a in H), flush=True)
    print(f"cand {c}: {len(found)} minimal sets, {sum(1 for v in found.values() if v is True)} valid at m=5", flush=True)
