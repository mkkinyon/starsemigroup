"""Relations among derived elements on K0 instances (ALWAYS-list), as k4rec6.py."""
import sys, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
INST = pickle.load(open('k0inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def rk(p): return sum(1 for B in p[0] if B & p[1])
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    u = theta(a, b); v = theta(b, a); p = theta(z, a); w = theta(y, c); q = theta(a, z); r = theta(y, a); s_ = theta(z, y); t = theta(z, c); cz = theta(c, z); yb = theta(b, y)
    T = {'a': a, 'b': b, 'c': c, 'y': y, 'z': z, 'u': u, 'v': v, 'p': p, 'w': w, 'q': q, 'r': r, 's': s_, 't': t, 'cz': cz, 'yb': yb}
    for e, f in itertools.combinations(T, 2):
        rec('%s ~ %s' % (e, f), commute(T[e], T[f])); rec('%s >< %s' % (e, f), matched(T[e], T[f]))
        rec('%s <= %s' % (e, f), theta(T[f], T[e]) == T[e]); rec('%s <= %s' % (f, e), theta(T[e], T[f]) == T[f])
        rec('th_%s(%s)=%s' % (e, f, e), theta(T[e], T[f]) == T[e]); rec('th_%s(%s)=%s' % (f, e, f), theta(T[f], T[e]) == T[f])
        rec('%s = %s' % (e, f), T[e] == T[f])
    for e in T: rec('rk %s = rk a' % e, rk(T[e]) == rk(a))
print(len(INST), 'instances; always-true relations (p=th_z(a), w=yc, q=th_a(z), r=th_y(a), s=th_z(y), t=th_z(c), cz=th_c(z), yb=th_b(y)):')
for k, (tot, ok) in sorted(stats.items()):
    if ok == tot: print('  ' + k)
