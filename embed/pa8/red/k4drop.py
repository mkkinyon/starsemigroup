"""Which K4 hypotheses are essential in P_4? Drop one at a time and count violations of a><b."""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = int(sys.argv[1]); P = projections(n); t0 = time.time()
le = lambda p, q: theta(q, p) == p
pairs = [(a, c) for a in P for c in P if matched(a, c)]
res = {}
def bump(k, viol):
    s = res.setdefault(k, [0, 0]); s[0] += 1; s[1] += viol
for a, c in pairs:
    Y3 = [y for y in P if theta(a, y) == a]           # drop y~c
    Y5 = [y for y in P if commute(y, c)]              # drop theta_a(y)=a
    Y = [y for y in Y3 if commute(y, c)]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a); ok = matched(a, b)
        Z4 = [z for z in P if theta(z, a) == u]                # drop b<=z
        Z7 = [z for z in P if le(b, z)]                        # drop theta_z(a)=u
        Z = [z for z in Z4 if le(b, z)]
        for z in Z:
            for y in Y:
                if theta(z, y) == v: bump('full', not ok)
                else: bump('drop h6 theta_z(y)=v', not ok)
            for y in Y3:
                if theta(z, y) == v and not commute(y, c): bump('drop h5 y~c', not ok)
            for y in Y5:
                if theta(z, y) == v and theta(a, y) != a: bump('drop h3 theta_a(y)=a', not ok)
        for z in Z4:
            if le(b, z): continue
            for y in Y:
                if theta(z, y) == v: bump('drop h4 b<=z', not ok)
        for z in Z7:
            if theta(z, a) == u: continue
            for y in Y:
                if theta(z, y) == v: bump('drop h7 theta_z(a)=u', not ok)
print('P_%d (%.0fs)' % (n, time.time() - t0))
for k, (tot, viol) in sorted(res.items()): print('  %-28s instances %7d  violations of a><b %6d' % (k, tot, viol))
