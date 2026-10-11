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
def blocks(p):
    out = []
    for b in p:
        top = frozenset(i for i in b if i < n)
        if top: out.append((top, any(i >= n for i in b)))
    return out
show = lambda p: '  '.join(('[' if t else '(') + ' '.join(map(str, sorted(bl))) + (']' if t else ')') for bl, t in blocks(p))
random.seed(1); done = 0
while True:
    a = random.choice(P); c = random.choice(P)
    if a == c or rank(a) < 1 or not mt(a, c): continue
    done += 1
    if done == 258: break
print("a =", show(a)); print("c =", show(c))
ident = [p for p in P if th(p, a) == th(p, c)]
dist = {}; frontier = [x for x in ident if comm(x, c)]
for x in frontier: dist[x] = 1
d = 1
while frontier:
    nxt = [z for z in ident if z not in dist and any(comm(y, z) for y in frontier)]
    d += 1
    for z in nxt: dist[z] = d
    frontier = nxt
far = [z for z, dd in dist.items() if dd == 4]
print(len(dist), "in component; distance-4 elements:", len(far))
for z in far: print("   z =", show(z))
E1ge = [x for x in ident if comm(x, c) and le(c, x)]
t0 = time.time(); bad = 0
for z in dist:
    Y = [y for y in ident if le(z, y)]
    if not any(comm(x, y) for x in E1ge for y in Y): bad += 1; print("   normal form FAILS for z =", show(z), "(distance", dist[z], ")")
print(f"normal form failures: {bad}/{len(dist)} ({time.time()-t0:.0f}s)")
# a distance-4 chain
z = far[0]
import itertools
for y3 in ident:
    if dist.get(y3) == 3 and comm(y3, z):
        for y2 in ident:
            if dist.get(y2) == 2 and comm(y2, y3):
                for y1 in ident:
                    if dist.get(y1) == 1 and comm(y1, y2):
                        print("chain: c ~", show(y1), " ~ ", show(y2), " ~ ", show(y3), " ~ z"); break
                else: continue
                break
        else: continue
        break
