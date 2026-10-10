import pickle, numpy as np, time, itertools
NAMES, bad, paths, closed = pickle.load(open('probe_bad.pkl', 'rb'))
NAMES2, SQ, SP, SR = pickle.load(open('probe_S.pkl', 'rb')); NA = len(NAMES)
# pack signatures into two uint64
def pack(m):
    bits = np.zeros(128, dtype=bool); bits[:NA] = m
    w = np.packbits(bits, bitorder='little').view(np.uint64); return int(w[0]), int(w[1])
B = np.zeros((len(bad), 2), dtype=np.uint64)
for k in range(len(bad)): B[k] = pack(bad[k])
# keep only maximal signatures? cheap heuristic: dedupe (already distinct). Use complement for test: G valid iff no row with (G & ~row)==0
NB0 = ~B[:, 0]; NB1 = ~B[:, 1]
def valid_p(g0, g1):
    return not np.any(((np.uint64(g0) & NB0) == 0) & ((np.uint64(g1) & NB1) == 0))
t0 = time.time()
PQ = {k: pack(m) for k, m in SQ.items()}; PP = {k: pack(m) for k, m in SP.items()}; PR = {k: pack(m) for k, m in SR.items()}
found = []; cnt = 0; lvl1 = 0
for k1, (a0, a1) in PQ.items():
    for k2, (b0, b1) in PP.items():
        g0, g1 = a0 & b0, a1 & b1
        if not valid_p(g0, g1): continue
        lvl1 += 1
        for k3, (c0, c1) in PR.items():
            h0, h1 = g0 & c0, g1 & c1; cnt += 1
            if valid_p(h0, h1): found.append((k1, k2, k3, h0, h1))
print("level-1 valid pairs:", lvl1, "triples tested:", cnt, "valid:", len(found), f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump(found, open('search_found.pkl', 'wb'))
def atoms(h0, h1):
    bits = np.unpackbits(np.array([h0, h1], dtype=np.uint64).view(np.uint8), bitorder='little')[:NA]
    return [NAMES[i] for i in np.nonzero(bits)[0]]
Gs = {}
for k1, k2, k3, h0, h1 in found: Gs.setdefault((h0, h1), []).append((k1, k2, k3))
res = sorted(((len(atoms(*k)), atoms(*k), v[:2], len(v)) for k, v in Gs.items()), key=lambda t: t[0])
for r in res[:25]: print(r)
