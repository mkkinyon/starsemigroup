"""Brute-force test of the abstract lemma: four labelled partitions a,b,c,d of [n] with
(L): N_a = N_b, or N_a \ N_b = {supp b}, N_b \ N_a = {supp a} (disjoint supports);
(R): same for c,d.  If Fine(a,c), Fine(b,c), Fine(b,d) then Fine(a,d)?"""
import sys, itertools
from pmon import all_set_partitions

def labelled(n):
    out = []
    for sp in all_set_partitions(list(range(n))):
        k = len(sp)
        for mask in range(1 << k):
            out.append(tuple((frozenset(b), bool(mask >> t & 1)) for t, b in enumerate(sp)))
    return out

def components(p, q):
    # union-find on points via blocks
    par = {}
    def find(x):
        while par.setdefault(x, x) != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for blocks in (p, q):
        for b, _ in blocks:
            b = list(b)
            for x in b[1:]: par[find(b[0])] = find(x)
    comp = {}
    for x in par: comp.setdefault(find(x), set()).add(x)
    return list(comp.values())

def fine(p, q):
    Tp = [b for b, t in p if t]; Tq = [b for b, t in q if t]
    for K in components(p, q):
        np_ = sum(1 for b in Tp if b <= K); nq = sum(1 for b in Tq if b <= K)
        if np_ > 1 or nq > 1 or (np_ != nq): return False
    return True

def cond_L(p, q):
    Np = {b for b, t in p if not t}; Nq = {b for b, t in q if not t}
    Sp = frozenset().union(*[b for b, t in p if t]) if any(t for _, t in p) else frozenset()
    Sq = frozenset().union(*[b for b, t in q if t]) if any(t for _, t in q) else frozenset()
    if Np == Nq: return True
    return Np - Nq == {Sq} and Nq - Np == {Sp} and not (Sp & Sq)

n = int(sys.argv[1]); L = labelled(n); print(len(L), "labelled partitions", flush=True)
cnt = 0; bad = 0
for a in L:
    for c in L:
        if not fine(a, c): continue
        for b in L:
            if not cond_L(a, b) or not fine(b, c): continue
            for d in L:
                if not cond_L(c, d) or not fine(b, d): continue
                cnt += 1
                if not fine(a, d):
                    bad += 1
                    if bad <= 3: print("COUNTEREXAMPLE", a, b, c, d)
print("instances", cnt, "bad", bad)
