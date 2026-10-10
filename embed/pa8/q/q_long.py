import pickle, numpy as np, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); n = 4
R = pickle.load(open('instQ4.pkl', 'rb')); rng = np.random.default_rng(1)
S = R[rng.choice(len(R), 30000, replace=False)]
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
L = 'acbdxy'
def ev(w, I):
    d = dict(zip(L, I)); r = d[w[0]]
    for ch in w[1:]: r = m(r, d[ch])
    return r
eqs = [('ad','acbd'), ('yad','yacbd'), ('xad','xacbd'), ('ad','abd'), ('yad','yabd'), ('xad','xabd'), ('ad','acd'), ('xad','xacd'), ('yad','yacd'),
       ('ab','acb'), ('yab','yacb'), ('xab','xacb'), ('cd','cbd'), ('ycd','ycbd'), ('xcd','xcbd'), ('cbd','cd'), ('acbd','acd'), ('yacbd','yacd'), ('xacbd','xacd'),
       ('xd','xbd'), ('xd','xcbd'), ('yd', 'ybd'), ('ac', 'ad'), ('ca','da'), ('xc','xcd'), ('cx','cdx'), ('yc','ycd'), ('ycx','ydx'), ('adx','acx'), ('ay','ayx')]
for l, r in eqs:
    bad = sum(1 for row in S if ev(l, [P[i] for i in row]) != ev(r, [P[i] for i in row]))
    print(f"{l} = {r}: fails {bad}")
