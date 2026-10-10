"""Word identities of length <= 5 over {a,c,x,y} on (W_2) instances (sample 3000, then all)."""
import sys, pickle, itertools, time, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
n = 4; inst = pickle.load(open('../rpp/w2inst4.pkl', 'rb')); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acxy'
words = [''.join(w) for k in range(1, 6) for w in itertools.product(L, repeat=k) if all(w[i] != w[i+1] for i in range(len(w)-1))]
print(len(words), 'words', flush=True)
def ev(w, V):
    r = V[w[0]]
    for ch in w[1:]: r = m(r, V[ch])
    return r
random.seed(1); sample = random.sample(inst, 3000)
eq = None; t0 = time.time()
for I in sample:
    V = dict(zip('acbxy', I)); vals = {}
    for w in words: vals.setdefault(ev(w, V), []).append(w)
    cur = {(w1, w2) for ws in vals.values() for w1, w2 in itertools.combinations(sorted(ws), 2)}
    eq = cur if eq is None else eq & cur
print(f"{len(eq)} equalities on the sample ({time.time()-t0:.0f}s)", flush=True)
for I in random.sample(inst, 60000):
    V = dict(zip('acbxy', I)); cache = {}
    def e(w):
        if w not in cache: cache[w] = ev(w, V)
        return cache[w]
    eq = {(w1, w2) for w1, w2 in eq if e(w1) == e(w2)}
print(f"{len(eq)} equalities on 60000 instances ({time.time()-t0:.0f}s)", flush=True)
parent = {w: w for w in words}
def find(w):
    while parent[w] != w: parent[w] = parent[parent[w]]; w = parent[w]
    return w
for w1, w2 in eq: parent[find(w1)] = find(w2)
cls = {}
for w in words: cls.setdefault(find(w), []).append(w)
for r, ws in sorted(cls.items(), key=lambda kv: (min(len(w) for w in kv[1]), sorted(kv[1], key=len)[0])):
    if len(ws) > 1: print(' = '.join(sorted(ws, key=lambda w: (len(w), w))[:12]) + (' ...' if len(ws) > 12 else ''))
