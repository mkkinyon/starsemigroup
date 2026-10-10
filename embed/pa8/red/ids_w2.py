"""Word identities (length <= 3) holding on all (R'_2) instances in P_4 (sampled first, then all)."""
import sys, pickle, itertools, time, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
n = 4; inst = pickle.load(open('../rpp/w2inst4.pkl', 'rb')); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbxy'
words = [''.join(w) for k in (1, 2, 3) for w in itertools.product(L, repeat=k) if all(w[i] != w[i+1] for i in range(len(w)-1))]
def ev(w, V):
    r = V[w[0]]
    for ch in w[1:]: r = m(r, V[ch])
    return r
random.seed(1); sample = random.sample(inst, 20000)
eq = None; t0 = time.time()
for I in sample:
    V = dict(zip(L, I)); vals = {w: ev(w, V) for w in words}
    cur = {(w1, w2) for w1, w2 in itertools.combinations(words, 2) if vals[w1] == vals[w2]}
    eq = cur if eq is None else eq & cur
print(f"{len(eq)} equalities on the sample ({time.time()-t0:.0f}s)", flush=True)
for I in inst:
    V = dict(zip(L, I))
    eq = {(w1, w2) for w1, w2 in eq if ev(w1, V) == ev(w2, V)}
print(f"{len(eq)} equalities on all {len(inst)} instances ({time.time()-t0:.0f}s)", flush=True)
# classes
parent = {w: w for w in words}
def find(w):
    while parent[w] != w: parent[w] = parent[parent[w]]; w = parent[w]
    return w
for w1, w2 in eq: parent[find(w1)] = find(w2)
cls = {}
for w in words: cls.setdefault(find(w), []).append(w)
for r, ws in sorted(cls.items(), key=lambda kv: (min(len(w) for w in kv[1]), kv[1])):
    if len(ws) > 1: print(' = '.join(sorted(ws, key=len)))
