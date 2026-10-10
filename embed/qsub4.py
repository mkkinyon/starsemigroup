import sys, time, itertools
import qsearch
from qsearch import Tq, sq, gens, q_of, canon
from analyse import props
from embed import PnData, find_embedding
def gen_sub(gs):
    S = set(gs); fr = list(S)
    while fr:
        new = []
        for a in list(S):
            for b in fr:
                for c in (Tq[a][b], Tq[b][a], sq[b]):
                    if c not in S: S.add(c); new.append(c)
        fr = new
    S = sorted(S); loc = {x: i for i, x in enumerate(S)}
    return [[loc[Tq[a][b]] for b in S] for a in S], [loc[sq[a]] for a in S], S
c, t, a0, b0 = gens
a1 = Tq[Tq[c][a0]][sq[c]]; a2 = Tq[Tq[c][a1]][sq[c]]
b1 = Tq[Tq[c][b0]][sq[c]]; b2 = Tq[Tq[c][b1]][sq[c]]
if __name__ == "__main__":
    nmax = int(sys.argv[1]); Ds = {k: PnData(k) for k in range(1, nmax + 1)}
    tests = {
     "<a0,a1,a2,b0,b1,b2>": [a0,a1,a2,b0,b1,b2],
     "<c,a0,b0>": [c,a0,b0],
     "<t,a0,b0>": [t,a0,b0],
     "<a0,b0,b1>": [a0,b0,b1],
     "<a0,a1,b0>": [a0,a1,b0],
     "<a0,b1,a1,b2>": [a0,b1,a1,b2],
     "<a0,a1,b0,b1>": [a0,a1,b0,b1],
     "<c,a0>": [c,a0], "<c,b0>": [c,b0], "<t,a0,a1,b0>": [t,a0,a1,b0],
     "<c,t,a0>": [c,t,a0], "<c,t,b0>": [c,t,b0],
    }
    for name, gs in tests.items():
        Ts, ss, S = gen_sub(gs); pr = props(Ts, ss)
        deg = None; tm = time.time()
        for m in range(1, nmax + 1):
            if find_embedding(Ts, ss, Ds[m]): deg = m; break
        print(f"{name}: size {len(S)}, nP={pr['nP']}, Q1={pr['Q1']}, inverse={pr['inverse']}, deg={deg} ({time.time()-tm:.0f}s)", flush=True)
