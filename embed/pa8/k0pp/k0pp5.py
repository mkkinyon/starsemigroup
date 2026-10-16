"""K0'' instances in P(P_5), random (a,c) pairs within a time budget; count violations of a><b."""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 5; budget = float(sys.argv[1]) if len(sys.argv) > 1 else 600
P = projections(n); random.seed(2); t0 = time.time()
pairs = [(a, c) for a in P for c in P if matched(a, c)]; random.shuffle(pairs)
tot = bad = neq = notk0 = np = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    np += 1
    Za = [z for z in P if theta(a, z) == a]
    Yc = [y for y in P if commute(y, c)]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        Y = [y for y in Yc if theta(y, b) == v]
        Z = [z for z in Za if theta(b, z) == b]
        for y in Y:
            for z in Z:
                if theta(y, z) != u: continue
                tot += 1
                if a != b: neq += 1
                if not matched(a, b): bad += 1
                if theta(z, a) != theta(z, b): notk0 += 1
print(f"P_5: {np} of {len(pairs)} (a,c) pairs, {tot} K0'' instances ({neq} with a != b), violations of a><b: {bad}, instances not satisfying theta_z(a)=theta_z(b): {notk0} ({time.time()-t0:.0f}s)")
