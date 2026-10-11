"""Distance from c to a in the identification graph I(a, c), in P_n."""
import sys, random
from collections import Counter
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = int(sys.argv[1]); P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
random.seed(0)
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 400)
cnt = Counter()
for a, c in pairs:
    ident = [p for p in P if th(p, a) == th(p, c)]
    dist = {c: 0}; frontier = [c]
    while frontier and a not in dist:
        nxt = [z for z in ident if z not in dist and any(comm(y, z) for y in frontier)]
        for z in nxt: dist[z] = dist[frontier[0]] + 1
        frontier = nxt
    cnt[dist.get(a, 'inf')] += 1
print(f"n={n}: distance from c to a over {len(pairs)} matched pairs: {dict(cnt)}")
