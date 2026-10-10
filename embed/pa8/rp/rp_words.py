"""Which word equations (words of length <=3 over a,b,c,x,y) hold in all (R') instances of P_n?"""
import sys, itertools, pickle, time
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
n = int(sys.argv[1]); inst = pickle.load(open(f'inst{n}.pkl', 'rb'))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbxy'
words = [w for l in (1, 2, 3) for w in itertools.product(L, repeat=l)]
def ev(w, I):
    d = dict(zip(L, I)); r = d[w[0]]
    for ch in w[1:]: r = m(r, d[ch])
    return r
# classes of words equal on all instances (union-find via signature on a sample, then verify)
t0 = time.time()
sample = inst[::max(1, len(inst)//3000)]
sig = {w: tuple(ev(w, I) for I in sample) for w in words}
classes = {}
for w in words: classes.setdefault(sig[w], []).append(w)
# verify on all instances
final = []
for ws in classes.values():
    if len(ws) < 2: continue
    groups = {}
    for I in inst:
        vals = {}
        for w in ws: vals.setdefault(ev(w, I), []).append(w)
        # refine: words with equal values across all instances; use a partition refinement
        for v, g in vals.items():
            pass
    # simple refinement
    part = [ws]
    for I in inst:
        newpart = []
        for g in part:
            d = {}
            for w in g: d.setdefault(ev(w, I), []).append(w)
            newpart.extend(d.values())
        part = newpart
        if all(len(g) == 1 for g in part): break
    final.extend(g for g in part if len(g) > 1)
print(f"{time.time()-t0:.0f}s")
for g in sorted(final, key=lambda g: (min(len(w) for w in g), g)):
    print(' = '.join(''.join(w) for w in sorted(g, key=lambda w: (len(w), w))))
