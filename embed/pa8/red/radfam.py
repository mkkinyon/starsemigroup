"""Radius lower bound construction: X = {p_1..p_k, q_1..q_k, t}; a = (p_1..p_k)(q_1)..(q_k)[t]; c = all singletons N except [t];
z = (p_1 q_1)...(p_k q_k)[t].  Claim: dist(c, z) = k+1 in the identification graph of (a, c) in P_{2k+1}.  Usage: python3 radfam.py k"""
import sys, time
from collections import deque
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
k = int(sys.argv[1]); n = 2 * k + 1; P = projections(n); memo = {}
def m_(p, q):
    kk = (p, q)
    if kk not in memo: memo[kk] = mul(p, q, n)
    return memo[kk]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
def build(bl):
    out = []
    for pts, t in bl:
        if t: out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    return tuple(sorted(out))
ps = list(range(k)); qs = list(range(k, 2 * k)); t = 2 * k
a = build([(set(ps), False)] + [({q}, False) for q in qs] + [({t}, True)])
c = build([({p}, False) for p in ps] + [({q}, False) for q in qs] + [({t}, True)])
z = build([({ps[i], qs[i]}, False) for i in range(k)] + [({t}, True)])
assert a in set(P) and c in set(P) and z in set(P)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
print(f"k={k}, n={n}: a|><|c {mt(a, c)}, z identifies {th(z, a) == th(z, c)}", flush=True)
t0 = time.time(); ident = [y for y in P if th(y, a) == th(y, c)]
print(f"{len(ident)} identifiers ({time.time()-t0:.0f}s)", flush=True)
dist = {c: 0}; dq = deque([c])
while dq:
    u = dq.popleft()
    if u == z: break
    for v in ident:
        if v not in dist and comm(u, v): dist[v] = dist[u] + 1; dq.append(v)
print(f"dist(c, z) = {dist.get(z, 'inf')}; component explored: {len(dist)} ({time.time()-t0:.0f}s)", flush=True)
