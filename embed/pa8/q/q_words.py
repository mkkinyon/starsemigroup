import pickle, numpy as np, itertools, sys, time
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); n = 4
R = pickle.load(open('instQ4.pkl', 'rb')); rng = np.random.default_rng(0)
S = R[rng.choice(len(R), 40000, replace=False)]
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbdxy'
words = [w for l in (1, 2, 3) for w in itertools.product(L, repeat=l)]
def ev(w, I):
    d = dict(zip(L, I)); r = d[w[0]]
    for ch in w[1:]: r = m(r, d[ch])
    return r
t0 = time.time()
part = [words]
for k, row in enumerate(S):
    I = [P[i] for i in row]
    newpart = []
    for g in part:
        if len(g) == 1: newpart.append(g); continue
        dd = {}
        for w in g: dd.setdefault(ev(w, I), []).append(w)
        newpart.extend(dd.values())
    part = newpart
    if k in (2000, 10000): print(k, "classes", len(part), f"({time.time()-t0:.0f}s)", flush=True)
print("classes", len(part), f"({time.time()-t0:.0f}s)")
for g in sorted((g for g in part if len(g) > 1), key=lambda g: (min(len(w) for w in g), g)):
    print(' = '.join(''.join(w) for w in sorted(g, key=lambda w: (len(w), w))))
