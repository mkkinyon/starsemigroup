"""Does the counting invariant suffice for (W_infinity)?  Test: a|><|c, b|><|c, y in Id(a,c), y~b,
delta(y)=delta(c) [and delta'(y)=0]  =>  a|><|b ?   Exhaustive in P_4; random pairs (a,c) in P_5 within a budget.
Usage: python3 deltaW.py n [budget]"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
def delta(x, a, c): return len(join(x, a)) - len(join(x, c))
def deltap(x, a, c): return sum(1 for K in join(x, a) if K & a[1]) - sum(1 for K in join(x, c) if K & c[1])
n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(2)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
t0 = time.time(); tried = 0; inst = 0; viol = 0; viol2 = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    tried += 1
    dc = delta(c, a, c)
    Y = [y for y in P if theta(y, a) == theta(y, c) and delta(y, a, c) == dc]
    B = [b for b in P if matched(b, c)]
    for y in Y:
        for b in B:
            if commute(y, b):
                inst += 1
                if not matched(a, b):
                    viol += 1
                    if deltap(y, a, c) == 0:
                        viol2 += 1
                        if viol2 <= 5: print('VIOLATION (delta and delta\'): a=%s c=%s y=%s b=%s' % (show(a, n), show(c, n), show(y, n), show(b, n)), flush=True)
print('P_%d: %d pairs (a,c), %d instances with delta(y)=delta(c); a|><|b fails in %d; of these %d also have delta\'(y)=0 (%.0fs)' % (n, tried, inst, viol, viol2, time.time() - t0))
