"""K0'': a><c><b, y~c, th_y(b)=v, th_y(z)=u, th_a(z)=a, th_b(z)=b => a><b, in P(P_4)."""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
P = projections(4); t0 = time.time(); tot = bad = 0; notk0 = 0
for a in P:
    for c in P:
        if not matched(a, c): continue
        Za = [z for z in P if theta(a, z) == a]
        for b in P:
            if not matched(b, c): continue
            u = theta(a, b); v = theta(b, a)
            Y = [y for y in P if commute(y, c) and theta(y, b) == v]
            Z = [z for z in Za if theta(b, z) == b]
            for y in Y:
                for z in Z:
                    if theta(y, z) != u: continue
                    tot += 1
                    if not matched(a, b): bad += 1
                    if theta(z, a) != theta(z, b): notk0 += 1
print('K0pp instances', tot, 'violations', bad, 'instances not satisfying th_z(a)=th_z(b):', notk0, '(%.0fs)' % (time.time() - t0))
