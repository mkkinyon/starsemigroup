import sys, pickle, time
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 4; P = projections(n); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m(m(x, p), x)
comm = lambda p, q: m(p, q) == m(q, p)
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
inst = pickle.load(open('../rpp/w2inst4.pkl', 'rb'))
Zc = {}   # (a,c) -> candidates z with c~z, z id
bad = []; t0 = time.time()
for a, c, b, x, y in inst:
    if (a, c) not in Zc: Zc[(a, c)] = [z for z in P if comm(z, c) and th(z, a) == th(z, c)]
    if not any(comm(z, b) for z in Zc[(a, c)]): bad.append((a, c, b, x, y))
print(f"instances with no z (c~z, z id, z~b): {len(bad)} of {len(inst)} ({time.time()-t0:.0f}s)")
from collections import Counter
print(Counter((rank(a), rank(c), rank(b), rank(x), rank(y)) for a, c, b, x, y in bad))
if bad:
    a, c, b, x, y = bad[0]
    for nm, p in zip('acbxy', bad[0]): print(nm, p)
