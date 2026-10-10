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
groups = {}
for a, c, b, x, y in inst: groups.setdefault((a, c, x, y), set()).add(b)
bad = []
for (a, c, x, y), Bs in groups.items():
    if not any(comm(z, c) and th(z, a) == th(z, c) and all(comm(z, b) for b in Bs) for z in P): bad.append((a, c, x, y, Bs))
print(len(bad), 'bad groups; ranks (a,c,x,y) distribution:')
from collections import Counter
print(Counter((rank(a), rank(c), rank(x), rank(y)) for a, c, x, y, Bs in bad))
print('a==c:', sum(1 for a, c, x, y, Bs in bad if a == c), ' x==y:', sum(1 for a, c, x, y, Bs in bad if x == y))
# retry in P_5: embed by adding point 4 as a singleton N-block (top 4, bottom 9)
n5 = 5; P5 = projections(n5); memo5 = {}
def m5(p, q):
    k = (p, q)
    if k not in memo5: memo5[k] = mul(p, q, n5)
    return memo5[k]
th5 = lambda x, p: m5(m5(x, p), x)
comm5 = lambda p, q: m5(p, q) == m5(q, p)
def emb(p):   # P_4 -> P_5: relabel bottom i+4 -> i+5, add singletons {4}, {9}
    return tuple(sorted([tuple(sorted(i if i < 4 else i + 1 for i in b)) for b in p] + [(4,), (9,)]))
t0 = time.time(); still = 0
for a, c, x, y, Bs in bad:
    a5, c5, Bs5 = emb(a), emb(c), [emb(b) for b in Bs]
    if not any(comm5(z, c5) and th5(z, a5) == th5(z, c5) and all(comm5(z, b) for b in Bs5) for z in P5): still += 1
print(f"still no z in P_5: {still} of {len(bad)} ({time.time()-t0:.0f}s)")
