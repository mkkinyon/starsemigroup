import sys, time, itertools
from qsub4 import gen_sub, a0, a1, a2, b0, b1, b2, Tq, sq
from analyse import props
from embed import PnData, find_embedding
nmax = int(sys.argv[1]); Ds = {k: PnData(k) for k in range(1, nmax + 1)}
names = {a0:'a0',a1:'a1',a2:'a2',b0:'b0',b1:'b1',b2:'b2'}
seen = {}
for k in (5,):
    for gs in itertools.combinations([a0,a1,a2,b0,b1,b2], k):
        Ts, ss, S = gen_sub(list(gs)); key = tuple(S)
        if key in seen: continue
        pr = props(Ts, ss); deg = None; tm = time.time()
        for m in range(1, nmax + 1):
            if find_embedding(Ts, ss, Ds[m]): deg = m; break
        seen[key] = deg
        print(f"<{[names[g] for g in gs]}>: size {len(S)}, nP={pr['nP']}, deg={deg} ({time.time()-tm:.0f}s)", flush=True)
