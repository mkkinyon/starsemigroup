"""Random check in P_6 (and P_7) of Lemma 5.40 (invariance under z<=w in Id) and of Theorem 5.45 in the form
y in Id(a,c), delta(y)=delta(c), delta'(y)=0, y~b, b|><|c => a|><|b.   Usage: python3 delta6.py n budget"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
def delta(x, a, c): return len(join(x, a)) - len(join(x, c))
def deltap(x, a, c): return sum(1 for K in join(x, a) if K & a[1]) - sum(1 for K in join(x, c) if K & c[1])
n = int(sys.argv[1]); budget = float(sys.argv[2]); P = projections(n); random.seed(7)
t0 = time.time(); inv = invbad = inst = viol = 0
while time.time() - t0 < budget:
    a = random.choice(P); c = random.choice(P)
    if not matched(a, c): continue
    dc = delta(c, a, c)
    # random identifier w and random z <= w (merge T(w)-blocks)
    for _ in range(200):
        w = random.choice(P)
        if theta(w, a) != theta(w, c): continue
        Tw = [B for B in w[0] if B & w[1]]; Nw = [B for B in w[0] if not (B & w[1])]
        random.shuffle(Tw); k = random.randint(1, max(1, len(Tw)))
        groups = [0] * k
        for B in Tw: groups[random.randrange(k)] |= B
        groups = [g for g in groups if g]
        T = sum(g for g in groups if random.random() < 0.5)
        z = (tuple(sorted(Nw + groups)), T)
        inv += 1
        if (delta(z, a, c), deltap(z, a, c)) != (delta(w, a, c), deltap(w, a, c)): invbad += 1; print('INVARIANCE FAILS', show(a,n), show(c,n), show(w,n), show(z,n))
        if (delta(w, a, c), deltap(w, a, c)) == (dc, 0):
            for b in random.sample(P, 300):
                if matched(b, c) and commute(w, b):
                    inst += 1
                    if not matched(a, b): viol += 1; print('VIOLATION', show(a,n), show(c,n), show(w,n), show(b,n))
print('P_%d: invariance tested on %d pairs (bad %d); end step tested on %d instances (violations %d) (%.0fs)' % (n, inv, invbad, inst, viol, time.time() - t0))
