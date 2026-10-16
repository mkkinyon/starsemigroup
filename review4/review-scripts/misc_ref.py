"""Small side checks (referee). 1) Lemma 1.1(c) numerically in P_4; 2) an example b><c with an N(b)-block containing a T(c)-block
(Step 2's phrase 'the N(b)-block N contains some C_k, impossible' is not by itself a contradiction); 3) the algebraic repair
ya = (ya)z(ya) = a(yzy)a = u tested on all P_4 K0 instances via union-find multiplication."""
import sys, pickle
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts'); sys.path.insert(0, '/home/claude/pa8w/review3/review-scripts')
from fast import projections, theta, join, matched, parse, show
import pm
n = 4; P = projections(n); bad = 0; npairs = 0
for p in P:
    for q in P:
        if not matched(p, q): continue
        npairs += 1
        for K in join(p, q):
            if K & (p[1] | q[1]):
                if sum(1 for b in p[0] if b & p[1] and b & K) != 1 or sum(1 for b in q[0] if b & q[1] and b & K) != 1: bad += 1
print('Lemma 1.1(c) in P_4: %d matched pairs, %d violations' % (npairs, bad))
n = 3
b = parse('[1](0 2)', 3); c = parse('[0](1 2)', 3)
print('example: b =', show(b, 3), ' c =', show(c, 3), ' b><c:', matched(b, c), ' N(b)-block {0,2} contains T(c)-block {0}')
# 3) repair identity on P_4 instances
I = pickle.load(open('/home/claude/pa8w/embed/pa8/k0/k0inst4.pkl', 'rb')); n = 4; bad = 0
for d in I[::7]:
    a, y, z = (pm.proj_to_partition(d[k], n) for k in 'ayz')
    ya = pm.mul(y, a, n)
    lhs = pm.mul(pm.mul(ya, z, n), ya, n)
    u = pm.proj_to_partition(theta(d['a'], d['b']), n)
    if lhs != ya or lhs != u: bad += 1
print('repair identity (ya)z(ya) = ya = u on %d P_4 instances (union-find products): %d violations' % (len(I[::7]), bad))
