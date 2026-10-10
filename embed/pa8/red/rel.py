import sys, pickle, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
n = 4; inst = pickle.load(open('rp2inst4.pkl', 'rb')); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def ev(w, V):
    r = V[w[0]]
    for ch in w[1:]: r = m(r, V[ch])
    return r
L = 'acbxzy'
le = lambda p, q, V: m(m(ev(q,V), ev(p,V)), ev(q,V)) == ev(p,V)      # p <= q
comm = lambda p, q, V: ev(p+q, V) == ev(q+p, V)
tests = {
 'cy = cxz': lambda V: ev('cy',V) == ev('cxz',V),
 'cy = cxzc': lambda V: ev('cy',V) == ev('cxzc',V),
 'xz <= y': lambda V: le('xz','y',V),
 'zcz <= x': lambda V: le('zcz','x',V),
 'zcz <= xc': lambda V: le('zcz','xc',V),
 'zcz = xzc': lambda V: ev('zcz',V) == ev('xzc',V),
 'zcz <= cy': lambda V: le('zcz','cy',V),
 'cy <= x': lambda V: le('cy','x',V),
 'x ~ y': lambda V: comm('x','y',V),
 'c ~ xz': lambda V: comm('c','xz',V),
 'y ~ xz': lambda V: comm('y','xz',V),
 'cxz = xzc': lambda V: ev('cxz',V)==ev('xzc',V),
 'aya = aza': lambda V: ev('aya',V)==ev('aza',V),
 'aya = axa': lambda V: ev('aya',V)==ev('axa',V),
 'axa = axza': lambda V: ev('axa',V)==ev('axza',V),
 'ab = acb': lambda V: ev('ab',V)==ev('acb',V),
 'xbx = ybx': lambda V: ev('xbx',V)==ev('ybx',V),
 'xb = xzb': lambda V: ev('xb',V)==ev('xzb',V),
 'xbx <= y': lambda V: le('xbx','y',V),
 'cy = c x z y c': lambda V: ev('cy',V)==ev('cxzyc',V),
 'theta_c(y) = theta_c(xzy)': lambda V: ev('cyc',V)==ev('cxzyc',V),
 'theta_a(x) = theta_a(y)': lambda V: ev('axa',V)==ev('aya',V),
 'theta_a(z) = theta_a(y)': lambda V: ev('aza',V)==ev('aya',V),
 'theta_a(xz) = theta_a(y)': lambda V: ev('axza',V)==ev('aya',V),
}
random.seed(2); S = random.sample(inst, 30000)
res = {k: 0 for k in tests}
for I in S:
    V = dict(zip(L, I))
    for k, f in tests.items():
        if not f(V): res[k] += 1
for k, v in res.items(): print(f"{k:32s} fails in {v} of {len(S)}")
