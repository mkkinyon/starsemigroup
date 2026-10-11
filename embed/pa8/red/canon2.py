"""Canonical first element x1' in Split(c): which cut of the N(c)-blocks works for all z in comp(c)?"""
import sys, time, random
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
def build(bl):
    out = []
    for pts, t in bl:
        if t: out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    return tuple(sorted(out))
part = lambda p: [pts for pts, t in blocks(p)]
def meetp(P1, P2): return [B & S for B in P1 for S in P2 if B & S]
def joinp(parts):
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
def cutT(p, sigma, keepN=lambda pts: False):   # cut N(p)-blocks by sigma into T-blocks, unless keepN(block)
    out = [(pts, True) for pts, t in blocks(p) if t]
    for pts, t in blocks(p):
        if t: continue
        if keepN(pts): out.append((pts, False))
        else: out += [(pts & S, True) for S in sigma if pts & S]
    return build(out)
singletons = [frozenset([u]) for u in range(n)]
CONS = {
 'cut N(c) into singletons': lambda a, c, z: cutT(c, singletons),
 'cut N(c) by eps_z': lambda a, c, z: cutT(c, part(z)),
 'cut N(c) by eps_a': lambda a, c, z: cutT(c, part(a)),
 'cut N(c) by eps_a ^ eps_z': lambda a, c, z: cutT(c, meetp(part(a), part(z))),
 'cut N(c) by eps_z, keep N(c)-blocks that are z-blocks': lambda a, c, z: cutT(c, part(z), keepN=lambda pts: pts in set(part(z))),
 'cut N(c) by singletons, keep N(c)-blocks that are N(z)-blocks': lambda a, c, z: cutT(c, singletons, keepN=lambda pts: (pts, False) in blocks(z)),
 'cut N(c) by singletons, keep N(c)-blocks inside N(z)-blocks': lambda a, c, z: cutT(c, singletons, keepN=lambda pts: any(pts <= q and not t for q, t in blocks(z))),
 'cut N(c) by eps_z, keep N(c)-blocks inside N(z)-blocks': lambda a, c, z: cutT(c, part(z), keepN=lambda pts: any(pts <= q and not t for q, t in blocks(z))),
}
random.seed(0); t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 200)
tot = hard_tot = 0; succ = {k: 0 for k in CONS}; succh = {k: 0 for k in CONS}; fails = {k: None for k in CONS}
for a, c in pairs:
    ident = lambda p: th(p, a) == th(p, c)
    I = [p for p in P if ident(p)]
    E1 = [x for x in I if comm(x, c)]; E2 = set(y for y in I if any(comm(x, y) for x in E1)); E3 = set(z for z in I if any(comm(y, z) for y in E2))
    for z in E3:
        tot += 1; hard = z not in E2; hard_tot += hard
        Y2 = [y for y in I if comm(y, z)]
        for k, f in CONS.items():
            x1 = f(a, c, z)
            if x1 in Pset and ident(x1) and comm(c, x1) and any(comm(x1, y) for y in Y2): succ[k] += 1; succh[k] += hard
            elif fails[k] is None: fails[k] = (a, c, z, x1, ident(x1) if x1 in Pset else None)
print(f"n={n}: {tot} (a,c,z), {hard_tot} hard ({time.time()-t0:.0f}s)")
show = lambda p: '  '.join(('[' if t else '(') + ' '.join(map(str, sorted(bl))) + (']' if t else ')') for bl, t in blocks(p))
for k in CONS:
    print(f"   {k:60s}: {succ[k]}/{tot} (hard {succh[k]}/{hard_tot})")
    if fails[k]: a, c, z, x1, idt = fails[k]; print(f"        fail: a = {show(a)}; c = {show(c)}; z = {show(z)}; x1' = {show(x1)} (identifies: {idt})")
