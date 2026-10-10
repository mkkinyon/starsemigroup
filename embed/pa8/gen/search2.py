import pickle, numpy as np, time
NAMES, bad, paths, closed = pickle.load(open('probe_bad.pkl', 'rb'))
NAMES2, SQ, SP, SR = pickle.load(open('probe_S.pkl', 'rb')); NA = len(NAMES)
EXCL = NAMES.index('p0|><|p3')
BAD = {'p0','p1','p2','p3','a','b','c'}
SQ = {k:v for k,v in SQ.items() if not (set(k)&BAD)}; SP = {k:v for k,v in SP.items() if not (set(k)&BAD)}; SR = {k:v for k,v in SR.items() if not (set(k[1:])&BAD)}
for D in (SQ, SP, SR):
    for k in D: D[k][EXCL] = False
rng = np.random.default_rng(0)
sub = bad[rng.choice(len(bad), size=120000, replace=False)]
def packrows(M):
    bits = np.zeros((len(M), 128), dtype=bool); bits[:, :NA] = M
    return np.packbits(bits, axis=1, bitorder='little').view(np.uint64)
B = packrows(sub); NB0 = ~B[:, 0]; NB1 = ~B[:, 1]
Bf = packrows(bad); NBf0 = ~Bf[:, 0]; NBf1 = ~Bf[:, 1]
def valid_p(g0, g1, full=False):
    if full: return not np.any(((g0 & NBf0) == 0) & ((g1 & NBf1) == 0))
    return not np.any(((g0 & NB0) == 0) & ((g1 & NB1) == 0))
def pack1(m): return packrows(m[None, :])[0]
t0 = time.time()
PQ = {k: pack1(m) for k, m in SQ.items()}; PP = {k: pack1(m) for k, m in SP.items()}; PR = {k: pack1(m) for k, m in SR.items()}
found = []; cnt = 0; lvl1 = 0; seen = set()
for k1, a in PQ.items():
    for k2, b in PP.items():
        g = a & b
        if not valid_p(g[0], g[1]): continue
        lvl1 += 1
        for k3, c in PR.items():
            h = g & c; key = (int(h[0]), int(h[1]))
            if key in seen: continue
            seen.add(key); cnt += 1
            if valid_p(h[0], h[1]) and valid_p(h[0], h[1], full=True): found.append((k1, k2, k3, key))
    print("k1", k1, "lvl1", lvl1, "distinct", cnt, "found", len(found), f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump(found, open('search2_found.pkl', 'wb'))
def atoms(h0, h1):
    bits = np.unpackbits(np.array([h0, h1], dtype=np.uint64).view(np.uint8), bitorder='little')[:NA]
    return [NAMES[i] for i in np.nonzero(bits)[0]]
Gs = {}
for k1, k2, k3, key in found: Gs.setdefault(key, []).append((k1, k2, k3))
res = sorted(((len(atoms(*k)), atoms(*k), v[:2], len(v)) for k, v in Gs.items()), key=lambda t: t[0])
for r in res[:25]: print(r)
