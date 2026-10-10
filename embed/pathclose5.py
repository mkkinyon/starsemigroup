"""Random-sampling verification of path-closing candidates in P(P_m) (paths sampled at random, all x)."""
import sys, json, time, random, numpy as np
from pa_embed2 import PPm
from pathclose import fmt
m = int(sys.argv[1]); n = int(sys.argv[2]); combos = json.load(open(sys.argv[3])); secs = float(sys.argv[4]) if len(sys.argv) > 4 else 300
D = PPm(m); N = D.N; tab = np.array(D.tab); TH = tab.T; ar = np.arange(N)
mt = (TH == ar[:, None]) & (TH.T == ar[None, :])
matched = {p: [q for q in range(N) if mt[p, q]] for p in range(N)}
V = ['p%d' % i for i in range(n + 1)]
alive = [tuple(tuple(a) for a in c) for c in combos]; refuted = {}
t0 = time.time(); npaths = 0
while time.time() - t0 < secs and alive:
    P = [random.randrange(N)]
    for _ in range(n): P.append(random.choice(matched[P[-1]]))
    if len(set(P)) < len(P) or mt[P[0], P[-1]]: continue
    npaths += 1
    cache = {}
    def atomvec(at):
        if at in cache: return cache[at]
        k = at[0]
        if k == 'comm': v = TH[:, P[at[1]]] == TH[P[at[1]], :]
        elif k == 'xle': v = TH[P[at[1]], :] == ar
        elif k == 'lex': v = TH[:, P[at[1]]] == P[at[1]]
        elif k == 'sees': v = TH[:, P[at[1]]] == TH[:, P[at[2]]]
        elif k == 'seen': v = TH[P[at[1]], :] == TH[P[at[2]], :]
        elif k == 'xeq': v = (TH[P[at[1]], P[at[2]]] == ar)
        v = v.copy(); v[list(P)] = False; cache[at] = v; return v
    still = []
    for c in alive:
        v = np.ones(N, bool)
        for at in c:
            v &= atomvec(at)
            if not v.any(): break
        if v.any(): refuted[c] = (P, int(np.nonzero(v)[0][0]))
        else: still.append(c)
    alive = still
print(f"m={m}, n={n}: {npaths} random open paths in {secs}s; refuted {len(refuted)} candidates:")
for c, w in refuted.items(): print("  ", [fmt(at, V) for at in c], "path", w[0], "x", w[1])
print("survivors:", len(alive))

json.dump([[list(a) for a in c] for c in alive], open(sys.argv[3].replace(".json","_surv.json"), "w"))
