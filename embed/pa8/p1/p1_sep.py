import pickle, numpy as np, sys, itertools
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); n = 4
R = pickle.load(open('instP4.pkl', 'rb'))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def maxA(projs, A): return max(sum(1 for Ai in A if Ai <= K) for K in join_classes(projs, n))
names = ['c', 'b', 'x', 'f=ab', 'u=xa', 'v=xc']
fails = {k: 0 for k in itertools.chain.from_iterable(itertools.combinations(range(len(names)), r) for r in range(0, 4))}
cnt = 0
for row in R:
    a, c, b, d, x = [P[i] for i in row]
    extra = [c, b, x, m(a, b), m(x, a), m(x, c)]
    A = [t for t, tr in top_blocks(a, n) if tr]
    if len(A) < 2: continue
    cnt += 1
    for key in fails:
        if maxA([a, d] + [extra[i] for i in key], A) > 1: fails[key] += 1
print("instances with >=2 A:", cnt)
for key, v in sorted(fails.items(), key=lambda kv: kv[1])[:20]: print(v, [names[i] for i in key])
