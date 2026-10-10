import pickle, numpy as np, sys, itertools
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); n = 4
R = pickle.load(open('instQ4.pkl', 'rb')); rng = np.random.default_rng(2)
S = R[rng.choice(len(R), 20000, replace=False)]
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
def maxA(projs, A):
    return max(sum(1 for Ai in A if Ai <= K) for K in join_classes(projs, n))
names = ['c', 'b', 'e=cd', 'x', 'y', 'u=ya', 'w=yb', 't=cxc', "u'=xa"]
fails = {k: 0 for k in itertools.chain.from_iterable(itertools.combinations(range(len(names)), r) for r in range(0, 3))}
for row in S:
    a, c, b, d, x, y = [P[i] for i in row]
    extra = [c, b, m(c, d), x, y, m(y, a), m(y, b), th(c, x), m(x, a)]
    A = [t for t, tr in top_blocks(a, n) if tr]
    if len(A) < 2: continue
    for key in fails:
        if maxA([a, d] + [extra[i] for i in key], A) > 1: fails[key] += 1
for key, v in sorted(fails.items(), key=lambda kv: kv[1]):
    print(v, [names[i] for i in key])
