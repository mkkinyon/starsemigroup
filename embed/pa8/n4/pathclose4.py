"""Sampled path-closing signature search, path length n with TWO auxiliaries (language of pathclose3.py),
auxiliaries restricted to the projections that commute with, or are restrictions of, some path element.
Usage: python3 pathclose4.py m n npaths seed   -> pc4sig_m_n_seed.pkl (atoms, neg signatures, pos signatures)"""
import sys, random, pickle, time, itertools, numpy as np
sys.path.insert(0, '/home/claude/pa8w/embed')
from pa_embed2 import PPm
from pathclose3 import atoms_for, fmt2

def signatures(m, n, npaths, seed, verbose=True):
    D = PPm(m); N = D.N; TH = np.array(D.tab).T; ar = np.arange(N)
    mt = (TH == ar[:, None]) & (TH.T == ar[None, :]); comm = TH == TH.T; le = TH.T == ar[:, None]
    matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
    atoms = atoms_for(n); nat = len(atoms)
    commXY = comm; xleY = le; ylex = (TH == ar[:, None])
    def atom_mat(at, P):
        if at[0] == 'ch': return np.broadcast_to(np.bool_(mt[P[at[1]], P[at[2]]]), (N, N))
        if at[0] in ('x', 'y'):
            z, k = at[0], at[1]
            if k == 'comm': v = TH[:, P[at[2]]] == TH[P[at[2]], :]
            elif k == 'zle': v = TH[P[at[2]], :] == ar
            elif k == 'lez': v = TH[:, P[at[2]]] == P[at[2]]
            elif k == 'sees': v = TH[:, P[at[2]]] == TH[:, P[at[3]]]
            elif k == 'seen': v = TH[P[at[2]], :] == TH[P[at[3]], :]
            elif k == 'zeq': v = TH[P[at[2]], P[at[3]]] == ar
            return np.broadcast_to(v[:, None] if z == 'x' else v[None, :], (N, N))
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
    rng = random.Random(seed); neg = set(); pos = set(); done = 0; t0 = time.time()
    while done < npaths:
        P = [rng.randrange(N)]; ok = True
        for i in range(n):
            nb = matched[P[-1]]
            if not nb: ok = False; break
            P.append(rng.choice(nb))
        if not ok or len(set(P)) < n + 1: continue
        done += 1
        aux = np.zeros(N, bool)
        for p in P: aux |= comm[:, p]; aux |= le[:, p]
        aux[P] = False
        keep = aux[:, None] & aux[None, :]; np.fill_diagonal(keep, False)
        M = np.stack([atom_mat(at, P)[keep] for at in atoms], axis=1)   # pairs x nat (bool)
        packed = np.packbits(M, axis=1)
        sigs = {row.tobytes() for row in packed}
        (pos if mt[P[0], P[-1]] else neg).update(sigs)
        if verbose and done % 500 == 0: print(f"  {done} paths, {len(neg)} neg, {len(pos)} pos sigs, {time.time()-t0:.0f}s", flush=True)
    pickle.dump(dict(atoms=atoms, neg=sorted(neg), pos=sorted(pos), m=m, n=n), open(f"pc4sig_{m}_{n}_{seed}.pkl", "wb"))
    return atoms, neg, pos

if __name__ == "__main__":
    m, n, npaths, seed = map(int, sys.argv[1:5])
    signatures(m, n, npaths, seed)
