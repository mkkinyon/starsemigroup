"""(L1c) core instances in P(P_5) for a random sample of triples a><c><b with a not>< b (time budget), saved to npy."""
import sys, time, random, numpy as np
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 600; seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
n = 5; P = projections(n); N = len(P); idx = {p: i for i, p in enumerate(P)}
t0 = time.time()
TH = np.array([[idx[theta(P[i], P[j])] for j in range(N)] for i in range(N)], dtype=np.int32)
MT = (TH == np.arange(N)[:, None]) & (TH.T == np.arange(N)[None, :])      # MT[i,j]: th_i(j)=i and th_j(i)=j
print('N =', N, 'tables (%.0fs)' % (time.time() - t0), flush=True)
triples = [(a, c, b) for a in range(N) for c in np.nonzero(MT[a])[0] for b in np.nonzero(MT[c])[0] if not MT[a, b]]
random.seed(seed); random.shuffle(triples); print(len(triples), 'triples with a not>< b', flush=True)
out = []; nt = 0
for a, c, b in triples:
    if time.time() - t0 > budget: break
    nt += 1; v = TH[b, a]
    g = (TH[c, :][:, None] == TH[:, a][None, :]) & (TH == v)        # [z, x]
    for z, x in zip(*np.nonzero(g)):
        gy = (TH[:, a] == TH[z, :]) & (TH[x, a] == TH[:, x])
        for y in np.nonzero(gy)[0]: out.append((a, c, b, int(x), int(y), int(z)))
print('%d triples scanned, %d instances (%.0fs)' % (nt, len(out), time.time() - t0))
np.save('l1c_inst5_s%d.npy' % seed, np.array(out, dtype=np.int16))
