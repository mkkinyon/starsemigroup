"""Canonical 3-chains: for z in comp(c) (identification graph), test constructions x1' = f(c, z, a), x2' = g(z, c, a) with
c ~ x1' ~ x2' ~ z, both identifying.  In P_n (n = 4 or 5, sampled pairs)."""
import sys, time, random, itertools
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = int(sys.argv[1]); P = projections(n); Pset = set(P); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
def blocks(p):
    out = []
    for b in p:
        top = frozenset(i for i in b if i < n)
        if top: out.append((top, any(i >= n for i in b)))
    return out
def build(bl):   # list of (frozenset, isT) -> pmon partition
    out = []
    for pts, t in bl:
        if t: out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    return tuple(sorted(out))
def part(p): return [pts for pts, t in blocks(p)]
def meet_split(B, sigma):   # split block B by partition sigma (list of frozensets)
    return [B & S for S in sigma if B & S]
def refine_T(p, sigma):     # N(p)-blocks split by sigma into T-blocks; T(p)-blocks kept
    return build([(pts, True) for pts, t in blocks(p) if t] + [(piece, True) for pts, t in blocks(p) if not t for piece in meet_split(pts, sigma)])
def refine_N(p, sigma):     # N(p)-blocks split by sigma into N-blocks
    return build([(pts, True) for pts, t in blocks(p) if t] + [(piece, False) for pts, t in blocks(p) if not t for piece in meet_split(pts, sigma)])
def allT(p): return build([(pts, True) for pts, t in blocks(p)])
def join_part(parts):
    parent = {u: u for u in range(n)}
    def f(u):
        while parent[u] != u: u = parent[u]
        return u
    for Pp in parts:
        for bl in Pp:
            bl = sorted(bl)
            for q in bl[1:]: parent[f(q)] = f(bl[0])
    cl = {}
    for u in range(n): cl.setdefault(f(u), set()).add(u)
    return [frozenset(s) for s in cl.values()]
CONS = {
 "x1'=refT(c,z), x2'=refT(z,c)": lambda a, c, z: (refine_T(c, part(z)), refine_T(z, part(c))),
 "x1'=refT(c,z), x2'=refT(z,c v... )": lambda a, c, z: (refine_T(c, part(z)), refine_T(z, part(a))),
 "x1'=refT(c,z^a), x2'=refT(z,c^a)": lambda a, c, z: (refine_T(c, join_part([part(z)]) and [B & S for B in part(z) for S in part(a) if B & S]), refine_T(z, [B & S for B in part(c) for S in part(a) if B & S])),
 "x1'=allT(c)?, x2'=allT(z)": lambda a, c, z: (allT(c), allT(z)),
 "x1'=refT(c,z), x2'=allT(z)": lambda a, c, z: (refine_T(c, part(z)), allT(z)),
}
random.seed(0); t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 300)
tot = 0; hard_tot = 0; succ = {k: 0 for k in CONS}; succ_hard = {k: 0 for k in CONS}
for a, c in pairs:
    ident = lambda p: th(p, a) == th(p, c)
    I = [p for p in P if ident(p)]
    E1 = [x for x in I if comm(x, c)]; E2 = set(y for y in I if any(comm(x, y) for x in E1)); E3 = set(z for z in I if any(comm(y, z) for y in E2))
    for z in E3:
        tot += 1; hard = z not in E2; hard_tot += hard
        for k, f in CONS.items():
            x1, x2 = f(a, c, z)
            if x1 in Pset and x2 in Pset and ident(x1) and ident(x2) and comm(c, x1) and comm(x1, x2) and comm(x2, z):
                succ[k] += 1; succ_hard[k] += hard
print(f"n={n}: {tot} (a,c,z) with z in comp, {hard_tot} needing 3 links ({time.time()-t0:.0f}s)")
for k in CONS: print(f"   {k:40s}: works for {succ[k]}/{tot}, hard: {succ_hard[k]}/{hard_tot}")
