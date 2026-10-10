import sys, pickle, itertools, time
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
n = int(sys.argv[1]); inst = pickle.load(open(sys.argv[3] if len(sys.argv) > 3 else f'inst{n}.pkl', 'rb')); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbxy'
def ev(w, V):
    r = V[w[0]]
    for ch in w[1:]: r = m(r, V[ch])
    return r
cands = [l.strip().split(' = ') for l in open(sys.argv[2]) if ' = ' in l]
pairs = [(cl[0], w) for cl in cands for w in cl[1:]]
fails = {p: 0 for p in pairs}; t0 = time.time()
for I in inst:
    V = dict(zip(L, I))
    for p in pairs:
        if ev(p[0], V) != ev(p[1], V): fails[p] += 1
print(f"{len(inst)} instances ({time.time()-t0:.0f}s)")
for p, f in fails.items(): print(p, 'FAILS', f) if f else None
print("holding:", [p for p, f in fails.items() if not f])
