"""Verify candidate path-closing hypothesis sets (lists of atoms) in P(P_m) with numpy over x. Prints survivors."""
import sys, json, itertools, numpy as np
from pa_embed2 import PPm
from pathclose import fmt

def check(m, n, combos, verbose=True):
    D = PPm(m); N = D.N; tab = np.array(D.tab)          # tab[x][y] = theta_y(x)
    TH = tab.T                                             # TH[p][q] = theta_p(q)
    mt = (TH == np.arange(N)[:, None]) & (TH.T == np.arange(N)[None, :])
    matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
    V = ['p%d' % i for i in range(n + 1)]
    def paths(prefix):
        if len(prefix) == n + 1:
            yield prefix; return
        for q in matched[prefix[-1]]:
            yield from paths(prefix + [q])
    alive = [tuple(tuple(a) for a in c) for c in combos]
    ar = np.arange(N)
    npaths = 0
    for p0 in range(N):
        for P in paths([p0]):
            if len(set(P)) < len(P) or mt[P[0], P[-1]]: continue
            npaths += 1
            cache = {}
            def atomvec(at):
                if at in cache: return cache[at]
                k = at[0]
                if k == 'comm': v = TH[:, P[at[1]]] == TH[P[at[1]], :]        # theta_x(p) == theta_p(x)
                elif k == 'xle': v = TH[P[at[1]], :] == ar                    # theta_p(x) == x
                elif k == 'lex': v = TH[:, P[at[1]]] == P[at[1]]             # theta_x(p) == p
                elif k == 'sees': v = TH[:, P[at[1]]] == TH[:, P[at[2]]]
                elif k == 'seen': v = TH[P[at[1]], :] == TH[P[at[2]], :]
                elif k == 'xeq': v = (TH[P[at[1]], P[at[2]]] == ar)
                v = v.copy(); v[list(P)] = False
                cache[at] = v; return v
            still = []
            for c in alive:
                v = np.ones(N, bool)
                for at in c:
                    v &= atomvec(at)
                    if not v.any(): break
                if v.any():
                    if verbose: print("  refuted:", [fmt(at, V) for at in c], "by path", P, "x =", int(np.nonzero(v)[0][0]), flush=True)
                else: still.append(c)
            alive = still
            if not alive: break
        if not alive: break
    if verbose:
        print(f"m={m}, n={n}: {npaths} open paths checked; survivors:")
        for c in alive: print("  ", [fmt(at, V) for at in c])
    return alive

if __name__ == "__main__":
    m = int(sys.argv[1]); n = int(sys.argv[2]); combos = json.loads(open(sys.argv[3]).read()) if len(sys.argv) > 3 else None
    check(m, n, combos)
