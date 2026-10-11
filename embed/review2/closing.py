"""Closing-lemma variants in P_m: for a|><|c|><|b, test which combinations of G1 (eps_c <= eps_a v eps_b), G1T (each T(c)-block in one
class of eps_a v eps_b), G2 (no class of eps_a v eps_b v eps_c with two T(c)-blocks) imply a|><|b."""
import sys
from fast import *
m = int(sys.argv[1])
P = projections(m)
def classes_of(*ps):
    cls = [1 << i for i in range(m)]
    for p in ps:
        for b in p[0]:
            merged = b; rest = []
            for c in cls:
                if c & b: merged |= c
                else: rest.append(c)
            rest.append(merged); cls = rest
    return cls
def tblocks(p): return [b for b in p[0] if b & p[1]]
cnt = {}
for a in P:
    for c in P:
        if a == c or not matched(a, c): continue
        for b in P:
            if b == c or not matched(b, c): continue
            ab = classes_of(a, b); abc = classes_of(a, b, c)
            G1 = all(any(bl & K == bl for K in ab) for bl in c[0])
            G1T = all(any(bl & K == bl for K in ab) for bl in tblocks(c))
            G2 = all(sum(1 for bl in tblocks(c) if bl & K) <= 1 for K in abc)
            G2ab = all(sum(1 for bl in tblocks(c) if bl & K) <= 1 for K in ab)   # weaker: classes of a v b only
            concl = matched(a, b)
            key = (G1, G1T, G2, G2ab, concl)
            cnt[key] = cnt.get(key, 0) + 1
for k in sorted(cnt): print('G1=%d G1T=%d G2=%d G2ab=%d  a|><|b=%d : %d' % (k + (cnt[k],)))
