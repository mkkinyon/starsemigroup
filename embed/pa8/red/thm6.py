"""Theorem 6 check: a|><|c|><|b, mu any grouping of the T(b)-blocks, m=(eps_b v mu) [labels irrelevant];
delta_ac(m)=kappa-|c| => (G1);  additionally delta'_ac(m)=0 => (G2) and a|><|b.   Usage: python3 thm6.py n [budget]"""
import sys, time, random, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
def delta(x, a, c): return len(join(x, a)) - len(join(x, c))
def deltap(x, a, c): return sum(1 for K in join(x, a) if K & a[1]) - sum(1 for K in join(x, c) if K & c[1])
def groupings(blocks):
    """all set partitions of a list of blocks (as masks): yield lists of merged masks"""
    if not blocks: yield []; return
    first, rest = blocks[0], blocks[1:]
    for sm in groupings(rest):
        for i in range(len(sm)): yield sm[:i] + [sm[i] | first] + sm[i+1:]
        yield [first] + sm
n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(3)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
t0 = time.time(); tried = 0; inst = 0; g1bad = 0; g2bad = 0; abbad = 0; inst2 = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    tried += 1; dc = delta(c, a, c)
    for b in P:
        if not matched(b, c): continue
        Tb = [B for B in b[0] if B & b[1]]; Nb = [B for B in b[0] if not (B & b[1])]
        for grp in groupings(Tb):
            m = (tuple(sorted(Nb + grp)), 0)
            if delta(m, a, c) != dc: continue
            inst += 1
            # (G1): every c-block inside a class of eps_a v eps_b
            jab = join(a, b)
            if not all(any(E & K == E for K in jab) for E in c[0]): g1bad += 1
            if deltap(m, a, c) != 0: continue
            inst2 += 1
            jabc = join(a, (jab, 0)) if False else None
            cls = join((tuple(jab), 0), c)
            if any(sum(1 for C in c[0] if (C & c[1]) and (C & K) for _ in [0]) > 1 for K in cls):
                pass
            if any(sum(1 for C in c[0] if (C & c[1]) and (C & K)) > 1 for K in cls): g2bad += 1
            if not matched(a, b):
                abbad += 1
                if abbad <= 3: print('VIOLATION a=%s c=%s b=%s m=%s' % (show(a, n), show(c, n), show(b, n), show(m, n)), flush=True)
print('P_%d: %d pairs (a,c); %d instances with delta(m)=delta(c): (G1) fails in %d; %d also have delta\'=0: (G2) fails in %d, a|><|b fails in %d (%.0fs)'
      % (n, tried, inst, g1bad, inst2, g2bad, abbad, time.time() - t0), flush=True)
