import sys, pickle, itertools, time
from qsub import gen_sub, projs2, q_of, elems, Tq, sq
from analyse import props
from embed import PnData, find_embedding
nmax = int(sys.argv[1])
Ds = {k: PnData(k) for k in range(1, nmax + 1)}
tested = {}
for k in (3, 4, 6):
    for gens in itertools.combinations(projs2, k):
        Ts, ss, S = gen_sub([q_of[g] for g in gens])
        key = tuple(S)
        if key in tested: continue
        pr = props(Ts, ss)
        deg = None; t = time.time()
        for m in Ds:
            if find_embedding(Ts, ss, Ds[m]): deg = m; break
        tested[key] = deg
        print(f"<{[elems[g] for g in gens]}>: size {len(S)}, nP={pr['nP']}, Q1={pr['Q1']}, deg={deg} ({time.time()-t:.0f}s)", flush=True)
