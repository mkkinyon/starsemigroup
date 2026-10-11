"""Radius of c's component in the identification-commutation graph, P_n, sampled (a,c)."""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = int(sys.argv[1]); N = int(sys.argv[2]); P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
t0 = time.time(); done = 0; maxr = 0
while done < N:
    a = random.choice(P); c = random.choice(P)
    if a == c or rank(a) < 1 or not mt(a, c): continue
    ident = [p for p in P if th(p, a) == th(p, c)]
    dist = {}; frontier = [x for x in ident if comm(x, c)]
    for x in frontier: dist[x] = 1
    d = 1
    while frontier:
        nxt = [z for z in ident if z not in dist and any(comm(y, z) for y in frontier)]
        d += 1
        for z in nxt: dist[z] = d
        frontier = nxt
    r = max(dist.values()) if dist else 0; maxr = max(maxr, r); done += 1
    print(f"pair {done}: rank a = {rank(a)}, |ident| = {len(ident)}, component size {len(dist)}, radius {r} ({time.time()-t0:.0f}s)", flush=True)
print("max radius:", maxr)
