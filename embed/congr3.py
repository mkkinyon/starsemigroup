import sys, time, pickle
from congr import all_congruences, quotient
from analyse import props
from embed import PnData, find_embedding
from pmon import partition_monoid, mul, star as pstar
n = 3
elems = partition_monoid(n); idx = {e: i for i, e in enumerate(elems)}
T = [[idx[mul(p, q, n)] for q in elems] for p in elems]
st = [idx[pstar(p, n)] for p in elems]
congs = all_congruences(T, st)
pickle.dump(congs, open("congs_P3.pkl", "wb"))
qs = []
for c in sorted(congs, key=lambda c: -len(set(c))):
    Tq, sq = quotient(T, st, c)
    pr = props(Tq, sq)
    print(f"quotient size {len(Tq)}: Q1={pr['Q1']} inverse={pr['inverse']} nP={pr['nP']}", flush=True)
    qs.append((Tq, sq, pr))
Ds = {k: PnData(k) for k in range(1, 6)}
for Tq, sq, pr in qs:
    if pr['Q1'] and not pr['inverse'] and len(Tq) < 203:
        deg = None
        for k in range(1, 6):
            if find_embedding(Tq, sq, Ds[k]): deg = k; break
        print(f"  Q1 quotient of size {len(Tq)}: deg = {deg}", flush=True)
