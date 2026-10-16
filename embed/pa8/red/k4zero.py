"""(K4^0): a><c><b, b<=z, th_z(c)=th_b(a), th_z(a)=th_a(b) => a><b, random sample of P(P_5)."""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 5; budget = float(sys.argv[1]) if len(sys.argv) > 1 else 300
P = projections(n); random.seed(3); t0 = time.time()
le = lambda p, q: theta(q, p) == p
pairs = [(a, c) for a in P for c in P if matched(a, c)]; random.shuffle(pairs)
tot = bad = np_ = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    np_ += 1
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a); ok = matched(a, b)
        for z in P:
            if le(b, z) and theta(z, c) == v and theta(z, a) == u:
                tot += 1
                if not ok: bad += 1
print(f'P_5: {np_} of {len(pairs)} pairs, {tot} instances, violations {bad} ({time.time()-t0:.0f}s)')
