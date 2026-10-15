import sys, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 4; P = projections(n)
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def rk(p): return sum(1 for B in p[0] if B & p[1])
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    u = theta(a, b); v = theta(b, a); w = theta(y, c); r = theta(y, a); rp = theta(y, z); ct = theta(c, u)
    T = {'a': a, 'b': b, 'c': c, 'y': y, 'z': z, 'u': u, 'v': v, 'w': w, 'r': r, "r'": rp, 'ct': ct}
    for p, q in itertools.combinations(T, 2):
        rec('%s ~ %s' % (p, q), commute(T[p], T[q]))
        rec('%s bowtie %s' % (p, q), matched(T[p], T[q]))
        rec('%s <= %s' % (p, q), theta(T[q], T[p]) == T[p])
        rec('%s <= %s' % (q, p), theta(T[p], T[q]) == T[q])
        rec('theta_%s(%s)=%s' % (p, q, p), theta(T[p], T[q]) == T[p])
        rec('theta_%s(%s)=%s' % (q, p, q), theta(T[q], T[p]) == T[q])
    rec('rk w = rk a', rk(w) == rk(a)); rec('rk w >= rk a', rk(w) >= rk(a)); rec('rk w <= rk a', rk(w) <= rk(a))
    rec('rk r = rk a', rk(r) == rk(a)); rec("rk r' = rk a", rk(rp) == rk(a))
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()):
    if ok == tot: print('  %-32s ALWAYS' % k)
