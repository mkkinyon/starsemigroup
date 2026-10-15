"""Replace y~c by weaker block conditions; count violations in P_4."""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = int(sys.argv[1]); P = projections(n); t0 = time.time()
le = lambda p, q: theta(q, p) == p
def lemY(c, y):  # every c-block inside a y-block or inside supp y
    return all(B & y[1] == B or any(Y & B == B for Y in y[0]) for B in c[0])
def lemY_T(c, y):  # every T(c)-block inside a y-block or inside supp y
    return all(B & y[1] == B or any(Y & B == B for Y in y[0]) for B in c[0] if B & c[1])
pairs = [(a, c) for a in P for c in P if matched(a, c)]
res = {}
def bump(k, viol):
    s = res.setdefault(k, [0, 0]); s[0] += 1; s[1] += viol
for a, c in pairs:
    Y3 = [y for y in P if theta(a, y) == a]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a); ok = matched(a, b)
        Z = [z for z in P if theta(z, a) == u and le(b, z)]
        for z in Z:
            for y in Y3:
                if theta(z, y) != v: continue
                if commute(y, c): continue
                ly, lyc, lT = lemY(c, y), lemY(c, y) and lemY(y, c), lemY_T(c, y)
                if ly: bump('h5 -> LemY(c in y)', not ok)
                if lyc: bump('h5 -> LemY both ways', not ok)
                if lT: bump('h5 -> LemY T(c) only', not ok)
                if ly and theta(y, c) == theta(c, y): bump('h5 -> LemY + th_y(c)=th_c(y)', not ok)
                if lemY(y, c): bump('h5 -> LemY(y in c)', not ok)
                if theta(c,y)==c: bump('h5 -> th_c(y)=c', not ok)
                if theta(y,c)==y: bump('h5 -> th_y(c)=y', not ok)
print('P_%d (%.0fs)' % (n, time.time() - t0))
for k, (tot, viol) in sorted(res.items()): print('  %-34s instances %7d  violations %6d' % (k, tot, viol))
