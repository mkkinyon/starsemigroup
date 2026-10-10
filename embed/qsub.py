import sys, pickle, itertools, time
from congr import quotient
from analyse import props
from embed import PnData, find_embedding
from pmon import partition_monoid, mul, star as pstar, rank
n = 3
elems = partition_monoid(n); idx = {e: i for i, e in enumerate(elems)}
T = [[idx[mul(p, q, n)] for q in elems] for p in elems]
st = [idx[pstar(p, n)] for p in elems]
congs = pickle.load(open("congs_P3.pkl", "rb"))
c103 = [c for c in congs if len(set(c)) == 103][0]
Tq, sq = quotient(T, st, c103)
# map from P_3 elements to quotient indices
classes = sorted(set(c103)); qidx = {cl: i for i, cl in enumerate(classes)}
q_of = [qidx[c103[x]] for x in range(len(T))]
def gen_sub(gens):
    S = set(gens); frontier = list(gens)
    while frontier:
        new = []
        for a in list(S):
            for b in frontier:
                for c in (Tq[a][b], Tq[b][a], sq[b]):
                    if c not in S: S.add(c); new.append(c)
        frontier = new
    S = sorted(S); loc = {x: i for i, x in enumerate(S)}
    return [[loc[Tq[a][b]] for b in S] for a in S], [loc[sq[a]] for a in S], S
projs2 = [x for x in range(len(T)) if rank(elems[x], n) == 2 and st[x] == x and T[x][x] == x]
print("rank-2 projections:", [elems[x] for x in projs2])
Ds = {k: PnData(k) for k in range(1, int(sys.argv[1]) + 1)} if __name__ == "__main__" else {}
if __name__ == "__main__":
    tested = set()
    for k in (1, 2):
        for gens in itertools.combinations(projs2, k):
            Ts, ss, S = gen_sub([q_of[g] for g in gens])
            key = tuple(S)
            if key in tested: continue
            tested.add(key)
            pr = props(Ts, ss)
            deg = None
            t = time.time()
            for m in Ds:
                if find_embedding(Ts, ss, Ds[m]): deg = m; break
            print(f"<{[elems[g] for g in gens]}>: size {len(S)}, Q1={pr['Q1']}, deg={deg} ({time.time()-t:.0f}s)", flush=True)
