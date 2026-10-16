"""Referee: what forces theta_y(a) = u = theta_a(b)?  Over all a><c><b in P_4 and all y, tabulate ya=u against
subsets of {H1: yc=cy, H2: theta_y(b)=v, H5': u<=y}.  (The proof asserts ya=u in Step 1 before theta_a(z)=a.)"""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import projections, theta, commute, matched
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
P = projections(n); t0 = time.time()
rows = {}
for a in P:
    for c in P:
        if not matched(a, c): continue
        for b in P:
            if not matched(c, b): continue
            u = theta(a, b); v = theta(b, a)
            for y in P:
                h1 = commute(y, c); h2 = theta(y, b) == v; h5 = theta(y, u) == u
                ok = theta(y, a) == u
                for name, cond in [('H5 only', h5), ('H5+H1', h5 and h1), ('H5+H2', h5 and h2), ('H5+H1+H2', h5 and h1 and h2), ('H1+H2', h1 and h2)]:
                    if cond:
                        r = rows.setdefault(name, [0, 0]); r[0] += 1
                        if not ok: r[1] += 1
print('P_%d (%.0fs): hypotheses kept -> instances, failures of theta_y(a)=u' % (n, time.time() - t0))
for k, (tot, bad) in rows.items(): print('  %-12s %9d  %9d' % (k, tot, bad))
