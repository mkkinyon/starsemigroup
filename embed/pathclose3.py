"""Path-closing search with TWO auxiliary projections x, y in P(P_m), WITH CHORD ATOMS p_i ~ p_j (non-consecutive
vertices, not the conclusion pair) -- pathclose2.py extended.
Path p_0 ~ ... ~ p_n (distinct vertices), x, y distinct and not vertices; conclusion p_0 ~ p_n.
Atoms: for z in {x,y}: comm(z,p_i), z<=p_i, p_i<=z, theta_z(p_i)=theta_z(p_j), theta_{p_i}(z)=theta_{p_j}(z), z=theta_{p_i}(p_j);
cross atoms: comm(x,y), x<=y, y<=x, theta_x(p_i)=theta_y(p_i), theta_{p_i}(x)=theta_{p_i}(y), x=theta_y(p_i), y=theta_x(p_i),
x=theta_{p_i}(y), y=theta_{p_i}(x).
Minimal non-vacuous valid hypothesis sets of size <= maxsize are printed and saved.  Usage: python3 pathclose2.py m n maxsize"""
import sys, json, itertools, numpy as np
from pa_embed2 import PPm

def atoms_for(n):
    A = []
    for z in ('x', 'y'):
        for i in range(n + 1): A += [(z, 'comm', i), (z, 'zle', i), (z, 'lez', i)]
        for i, j in itertools.combinations(range(n + 1), 2): A += [(z, 'sees', i, j), (z, 'seen', i, j)]
        for i in range(n + 1):
            for j in range(n + 1):
                if i != j: A.append((z, 'zeq', i, j))
    for i, j in itertools.combinations(range(n + 1), 2):
        if j - i >= 2 and (i, j) != (0, n): A.append(('ch', i, j))
    A += [('xy', 'comm'), ('xy', 'xley'), ('xy', 'ylex')]
    for i in range(n + 1): A += [('xy', 'sees', i), ('xy', 'seen', i), ('xy', 'x=th_y', i), ('xy', 'y=th_x', i), ('xy', 'x=th_p_y', i), ('xy', 'y=th_p_x', i)]
    return A

def fmt2(at, V):
    if at[0] == 'ch': return f"{V[at[1]]}~{V[at[2]]}"
    if at[0] in ('x', 'y'):
        z, k = at[0], at[1]
        if k == 'comm': return f"{z}{V[at[2]]}={V[at[2]]}{z}"
        if k == 'zle': return f"{z}<={V[at[2]]}"
        if k == 'lez': return f"{V[at[2]]}<={z}"
        if k == 'sees': return f"th_{z}({V[at[2]]})=th_{z}({V[at[3]]})"
        if k == 'seen': return f"th_{V[at[2]]}({z})=th_{V[at[3]]}({z})"
        if k == 'zeq': return f"{z}=th_{V[at[2]]}({V[at[3]]})"
    k = at[1]
    if k == 'comm': return "xy=yx"
    if k == 'xley': return "x<=y"
    if k == 'ylex': return "y<=x"
    if k == 'sees': return f"th_x({V[at[2]]})=th_y({V[at[2]]})"
    if k == 'seen': return f"th_{V[at[2]]}(x)=th_{V[at[2]]}(y)"
    if k == 'x=th_y': return f"x=th_y({V[at[2]]})"
    if k == 'y=th_x': return f"y=th_x({V[at[2]]})"
    if k == 'x=th_p_y': return f"x=th_{V[at[2]]}(y)"
    if k == 'y=th_p_x': return f"y=th_{V[at[2]]}(x)"

def run(m, n, maxsize, verbose=True):
    D = PPm(m); N = D.N; TH = np.array(D.tab).T; ar = np.arange(N)     # TH[p][q] = theta_p(q)
    mt = (TH == ar[:, None]) & (TH.T == ar[None, :])
    matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
    V = ['p%d' % i for i in range(n + 1)]; atoms = atoms_for(n); nat = len(atoms)
    # path-independent cross matrices (x rows, y columns)
    commXY = TH == TH.T
    xleY = (TH.T == ar[:, None])      # theta_y(x) == x  : TH[y][x] == x  -> as [x,y]: TH.T[x,y] = TH[y,x]
    ylex = (TH == ar[:, None])        # theta_x(y) == y  : TH[x][y] == y
    def paths(prefix):
        if len(prefix) == n + 1:
            yield prefix; return
        for q in matched[prefix[-1]]:
            yield from paths(prefix + [q])
    def atom_mat(at, P):
        """boolean N x N matrix over (x, y)"""
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
        if k == 'x=th_y': return TH[:, i][None, :] == ar[:, None]      # TH[y][i] == x
        if k == 'y=th_x': return TH[:, i][:, None] == ar[None, :]      # TH[x][i] == y
        if k == 'x=th_p_y': return TH[i, :][None, :] == ar[:, None]    # TH[i][y] == x
        if k == 'y=th_p_x': return TH[i, :][:, None] == ar[None, :]    # TH[i][x] == y
    neg = set(); pos = set(); npaths = 0
    lo = min(nat, 62); hi = nat - lo
    w1 = (1 << np.arange(lo, dtype=np.int64)).astype(np.uint64); w2 = (1 << np.arange(max(hi, 1), dtype=np.int64)).astype(np.uint64)
    for p0 in range(N):
        for P in paths([p0]):
            if len(set(P)) < len(P): continue
            npaths += 1
            keep = np.ones((N, N), bool); keep[list(P), :] = False; keep[:, list(P)] = False; np.fill_diagonal(keep, False)
            mats = [atom_mat(at, P)[keep] for at in atoms]          # each a vector over valid (x,y) pairs
            M = np.stack(mats, axis=1).astype(np.uint64)             # pairs x nat
            s1 = M[:, :lo] @ w1
            s2 = M[:, lo:] @ w2[:hi] if hi else np.zeros(M.shape[0], np.uint64)
            pairs = np.unique(np.stack([s1, s2], axis=1), axis=0)
            sigs = {int(a) | (int(b) << lo) for a, b in pairs}
            (pos if mt[P[0], P[-1]] else neg).update(sigs)
    negl = sorted(neg, key=lambda s: -bin(s).count('1')); maxs = []
    for s in negl:
        if not any((s & t) == s for t in maxs): maxs.append(s)
    if verbose: print(f"m={m}, n={n}: {npaths} paths, {len(neg)} negative signatures, {len(maxs)} maximal, {len(pos)} positive; {nat} atoms", flush=True)
    import pickle; pickle.dump(dict(atoms=atoms, maxs=maxs, pos=sorted(pos)), open(f"pc3sig_{m}_{n}.pkl", "wb"))
    out = []
    for size in range(1, maxsize + 1):
        for combo in itertools.combinations(range(nat), size):
            H = sum(1 << k for k in combo)
            if any((H & s) == H for s in maxs): continue
            if any((h & H) == h for h in out): continue
            if not any((H & s) == H for s in pos): continue
            out.append(H)
            if verbose: print("  ", size, [fmt2(atoms[k], V) for k in combo], flush=True)
    json.dump([[list(atoms[k]) for k in range(nat) if H >> k & 1] for H in out], open(f"pc3_{m}_{n}.json", "w"))
    return atoms, out

if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
