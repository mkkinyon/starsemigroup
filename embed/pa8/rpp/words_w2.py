"""Which equalities among short words hold on all (R'') instances of P_n?"""
import sys, pickle, itertools, time
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
n = int(sys.argv[1]); inst = pickle.load(open(f'w2inst{n}.pkl', 'rb')); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbxy'
words = [w for k in (1, 2, 3) for w in itertools.product(L, repeat=k)]
words = [''.join(w) for w in words if all(w[i] != w[i+1] for i in range(len(w)-1))]
def ev(w, V):
    r = V[w[0]]
    for ch in w[1:]: r = m(r, V[ch])
    return r
eq = None; t0 = time.time()
import random; random.seed(1); sample = inst if len(sys.argv) < 3 else random.sample(inst, int(sys.argv[2]))
for I in sample:
    V = dict(zip(L, I))
    vals = {w: ev(w, V) for w in words}
    cur = {(w1, w2) for w1, w2 in itertools.combinations(words, 2) if vals[w1] == vals[w2]}
    eq = cur if eq is None else eq & cur
    if not eq: break
print(f"{len(eq)} equalities on all {len(sample)} instances ({time.time()-t0:.0f}s)")
# print a reduced list: group by union-find, show classes
parent = {w: w for w in words}
def find(w):
    while parent[w] != w: parent[w] = parent[parent[w]]; w = parent[w]
    return w
for w1, w2 in eq: parent[find(w1)] = find(w2)
cl = {}
for w in words: cl.setdefault(find(w), []).append(w)
for k, v in sorted(cl.items(), key=lambda kv: (min(len(w) for w in kv[1]), kv[1][0])):
    if len(v) > 1: print(' = '.join(sorted(v, key=len)))
