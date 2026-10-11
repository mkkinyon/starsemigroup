"""Look for a term construction shortening a 4-chain c~x1~x2~x3~x4 (all identifying) to a 3-chain c~x1'~x2'~x4, in P_4."""
import sys, time, itertools, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 4; P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
random.seed(0)
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
# collect 4-chains where x4 is not in E2 (the interesting ones), plus a sample of others
chains = []; t0 = time.time()
for a, c in pairs:
    ident = [p for p in P if th(p, a) == th(p, c)]
    E1 = [x for x in ident if comm(x, c)]
    E2 = set(y for y in ident if any(comm(x, y) for x in E1))
    E3 = set(z for z in ident if any(comm(y, z) for y in E2))
    hard = E3 - E2
    if not hard: continue
    for x1 in E1:
        for x2 in ident:
            if not comm(x1, x2): continue
            for x3 in ident:
                if not comm(x2, x3): continue
                for x4 in hard:
                    if comm(x3, x4): chains.append((a, c, x1, x2, x3, x4))
print(len(chains), '4-chains to elements needing 3 links', f"({time.time()-t0:.0f}s)", flush=True)
# candidate terms for x2' (must commute with x4 and identify), x1' (commute with c, identify, commute with x2')
def terms(a, c, x1, x2, x3, x4):
    T = {'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4, 'c': c, 'a': a}
    out = {}
    names = list(T)
    for p in names:
        for q in names:
            if p != q: out[f'th_{p}({q})'] = th(T[p], T[q])
    for p in names: out[p] = T[p]
    return out
ok = {}
sample = random.sample(chains, min(400, len(chains)))
for ch in sample:
    a, c, x1, x2, x3, x4 = ch; tm = terms(*ch); ident = lambda p: th(p, a) == th(p, c)
    good2 = [k for k, v in tm.items() if ident(v) and comm(v, x4)]
    for k2 in good2:
        v2 = tm[k2]
        for k1, v1 in tm.items():
            if ident(v1) and comm(v1, c) and comm(v1, v2):
                ok[(k1, k2)] = ok.get((k1, k2), 0) + 1
best = sorted(ok.items(), key=lambda kv: -kv[1])[:15]
print(f"of {len(sample)} sampled chains, term pairs (x1', x2') that work:")
for (k1, k2), cnt in best: print(f"   x1' = {k1:12s} x2' = {k2:12s}: {cnt}")
