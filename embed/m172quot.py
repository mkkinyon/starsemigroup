import sys, time
from collections import defaultdict
from pmon import partition_monoid, mul, star, rank, canon, is_projection
from pa_embed2 import embed
M = [[0,0,0,3,3,3],[0,1,0,3,3,5],[0,0,2,3,4,5],[0,0,0,3,3,3],[0,0,2,3,4,3],[0,1,2,3,3,5]]
for n in (3, 4):
    elems = partition_monoid(n); idx = {e: i for i, e in enumerate(elems)}; N = len(elems)
    rk = [rank(e, n) for e in elems]
    def hat(p):
        out = []
        for b in p:
            up = [x for x in b if x < n]; lo = [x for x in b if x >= n]
            if up and lo: out += [tuple(up), tuple(lo)]
            else: out.append(tuple(b))
        return tuple(sorted(out))
    for variant in (1, 2):
        key = {}; cls = list(range(N))
        for i, e in enumerate(elems):
            if rk[i] <= 1: k = ("hat", hat(e))
            elif variant == 2 and rk[i] == 2:
                up = tuple(sorted(tuple(x for x in b if x < n) for b in e if any(x < n for x in b)))
                lo = tuple(sorted(tuple(x for x in b if x >= n) for b in e if any(x >= n for x in b)))
                tu = tuple(sorted(tuple(x for x in b if x < n) for b in e if any(x < n for x in b) and any(x >= n for x in b)))
                tl = tuple(sorted(tuple(x for x in b if x >= n) for b in e if any(x < n for x in b) and any(x >= n for x in b)))
                k = ("H", up, lo, tu, tl)
            else: k = ("id", i)
            key.setdefault(k, i); cls[i] = key[k]
        projs = sorted({cls[i] for i, e in enumerate(elems) if is_projection(e, n)})
        pidx = {c: k for k, c in enumerate(projs)}
        T = [[pidx[cls[idx[mul(mul(elems[y], elems[x], n), elems[y], n)]]] for y in projs] for x in projs]
        class D: pass
        D.tab = T; D.N = len(projs); D.reps = range(len(projs))
        r = embed(M, D)
        print(f"P_{n} variant {variant}: {len(projs)} projections; M172 embeds: {r is not None}")
        if r: print("   ", [elems[projs[v]] for v in r])
