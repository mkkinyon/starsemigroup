import sys, time, itertools
from qsub4 import gen_sub, a0, a1, a2, b0, b1, b2, Tq, sq
from analyse import props
from embed import PnData, find_embedding
z = Tq[b0][b1]; w = Tq[a0][a1]; m0 = Tq[a0][b0]; m1 = Tq[a1][b1]; m2 = Tq[a2][b2]
names = {a0:'a0',a1:'a1',a2:'a2',b0:'b0',b1:'b1',b2:'b2',z:'z',w:'w',m0:'m0',m1:'m1',m2:'m2'}
allp = [a0,a1,a2,b0,b1,b2,z,w,m0,m1,m2]
nmax = int(sys.argv[1]); Ds = {k: PnData(k) for k in range(1, nmax + 1)}
seen = {}
for k in (3, 4):
    for gs in itertools.combinations(allp, k):
        if not any(g in (z,w,m0,m1,m2) for g in gs): continue    # need a band projection
        Ts, ss, S = gen_sub(list(gs)); key = tuple(S)
        if key in seen: continue
        deg = None; tm = time.time()
        for m in range(1, nmax + 1):
            if find_embedding(Ts, ss, Ds[m]): deg = m; break
        seen[key] = deg
        if deg is None or deg >= 4:
            print(f"<{[names[g] for g in gs]}>: size {len(S)}, nP={props(Ts,ss)['nP']}, deg={deg} ({time.time()-tm:.0f}s)", flush=True)
print("done; tested", len(seen), "distinct subsemigroups")
