"""Sampled path-closing signature search, path length n, two auxiliaries x, y, reduced atom language (78 atoms for n=4).
Auxiliaries range over projections commuting with or below some path element.  Rows (signatures) are written as
packed bitstrings to pc4_<m>_<n>_<seed>.neg / .pos (one record = ceil(nat/8) bytes), deduplicated per path.
Usage: python3 pathclose4b.py m n npaths seed"""
import sys, random, time, itertools, numpy as np
sys.path.insert(0, '/home/claude/pa8w/embed')
from pa_embed2 import PPm

def atoms_for(n):
    A = []
    for z in ('x', 'y'):
        for i in range(n + 1): A.append((z, 'comm', i))
        for i in range(n + 1): A.append((z, 'zle', i))
        for i, j in itertools.combinations(range(n + 1), 2): A.append((z, 'sees', i, j))
        for i, j in itertools.combinations(range(n + 1), 2): A.append((z, 'seen', i, j))
    A += [('xy', 'comm'), ('xy', 'xley'), ('xy', 'ylex')]
    for i in range(n + 1): A.append(('xy', 'sees', i))
    for i in range(n + 1): A.append(('xy', 'seen', i))
    for i in range(n + 1):
        for j in range(n + 1):
            if i != j: A.append(('xy', 'xsees', i, j)); A.append(('xy', 'xseen', i, j))
    for i, j in itertools.combinations(range(n + 1), 2):
        if j - i >= 2 and (i, j) != (0, n): A.append(('ch', i, j))
    return A

def fmt(at, V=None):
    V = V or ['p%d' % i for i in range(10)]
    if at[0] == 'ch': return f"{V[at[1]]}~{V[at[2]]}"
    if at[0] in ('x', 'y'):
        z, k = at[0], at[1]
        if k == 'comm': return f"{z}{V[at[2]]}={V[at[2]]}{z}"
        if k == 'zle': return f"{z}<={V[at[2]]}"
        if k == 'sees': return f"th_{z}({V[at[2]]})=th_{z}({V[at[3]]})"
        if k == 'seen': return f"th_{V[at[2]]}({z})=th_{V[at[3]]}({z})"
    k = at[1]
    if k == 'comm': return "xy=yx"
    if k == 'xley': return "x<=y"
    if k == 'ylex': return "y<=x"
    if k == 'sees': return f"th_x({V[at[2]]})=th_y({V[at[2]]})"
    if k == 'seen': return f"th_{V[at[2]]}(x)=th_{V[at[2]]}(y)"
    if k == 'xsees': return f"th_x({V[at[2]]})=th_y({V[at[3]]})"
    if k == 'xseen': return f"th_{V[at[2]]}(x)=th_{V[at[3]]}(y)"

def run(m, n, npaths, seed, verbose=True):
    D = PPm(m); N = D.N; TH = np.array(D.tab).T; ar = np.arange(N)
    mt = (TH == ar[:, None]) & (TH.T == ar[None, :]); comm = TH == TH.T; le = TH.T == ar[:, None]
    matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
    atoms = atoms_for(n); nat = len(atoms)
    def atom_mat(at, P):
        if at[0] == 'ch': return np.broadcast_to(np.bool_(mt[P[at[1]], P[at[2]]]), (N, N))
        if at[0] in ('x', 'y'):
            z, k = at[0], at[1]
            if k == 'comm': v = TH[:, P[at[2]]] == TH[P[at[2]], :]
            elif k == 'zle': v = TH[P[at[2]], :] == ar
            elif k == 'sees': v = TH[:, P[at[2]]] == TH[:, P[at[3]]]
            elif k == 'seen': v = TH[P[at[2]], :] == TH[P[at[3]], :]
            return np.broadcast_to(v[:, None] if z == 'x' else v[None, :], (N, N))
        k = at[1]
        if k == 'comm': return comm
        if k == 'xley': return le
        if k == 'ylex': return (TH == ar[:, None])
        i = P[at[2]]
        if k == 'sees': return TH[:, i][:, None] == TH[:, i][None, :]
        if k == 'seen': return TH[i, :][:, None] == TH[i, :][None, :]
        j = P[at[3]]
        if k == 'xsees': return TH[:, i][:, None] == TH[:, j][None, :]
        if k == 'xseen': return TH[i, :][:, None] == TH[j, :][None, :]
    rng = random.Random(seed); done = 0; t0 = time.time(); nneg = npos = 0
    fneg = open(f"pc4_{m}_{n}_{seed}.neg", "wb"); fpos = open(f"pc4_{m}_{n}_{seed}.pos", "wb")
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
        aux[P] = True
        keep = aux[:, None] & aux[None, :]
        M = np.stack([atom_mat(at, P)[keep] for at in atoms], axis=1)
        packed = np.unique(np.packbits(M, axis=1), axis=0)
        if mt[P[0], P[-1]]: fpos.write(packed.tobytes()); npos += len(packed)
        else: fneg.write(packed.tobytes()); nneg += len(packed)
        if verbose and done % 500 == 0: print(f"  {done} paths, {nneg} neg rows, {npos} pos rows, {time.time()-t0:.0f}s", flush=True)
    fneg.close(); fpos.close()
    print("done", done, nneg, npos, "atoms", nat, "bytes/rec", (nat + 7) // 8)

if __name__ == "__main__":
    m, n, npaths, seed = map(int, sys.argv[1:5])
    run(m, n, npaths, seed)
