"""Normal form c <= x1 ~ x2 >= z for all z in comp(c), sampled (a, c) in P_6."""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 6; P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
mt = lambda p, q: th(p, q) == p and th(q, p) == q; le = lambda p, q: th(q, p) == p
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
random.seed(int(sys.argv[1])); t0 = time.time(); done = 0; bad = 0; tot = 0
while done < int(sys.argv[2]):
    a = random.choice(P); c = random.choice(P)
    if a == c or rank(a) < 1 or not mt(a, c): continue
    ident = [p for p in P if th(p, a) == th(p, c)]
    E1 = [x for x in ident if comm(x, c)]; comp = set(E1); frontier = list(E1)
    while frontier:
        nxt = [z for z in ident if z not in comp and any(comm(y, z) for y in frontier)]
        comp |= set(nxt); frontier = nxt
    E1ge = [x for x in E1 if le(c, x)]
    for z in comp:
        tot += 1
        Y = [y for y in ident if le(z, y)]
        if not any(comm(x, y) for x in E1ge for y in Y): bad += 1; print("  FAIL", a, c, z, flush=True)
    done += 1
    print(f"pair {done}: comp size {len(comp)}, failures so far {bad}/{tot} ({time.time()-t0:.0f}s)", flush=True)
