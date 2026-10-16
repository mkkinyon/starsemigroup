"""Test of the Step-2 claim of Thm 5.49, 'every B_i lies in some S_j' (equivalently supp theta_b(a) = supp b, i.e.
theta_b(a) has no N-block inside supp b), and of the counting identity used to derive it,
   |eps_v|_{supp b} = |eps_v v eps_c|_{supp c}   (v = theta_b(a)),  'the left side is n'.
(1) With only a|><|c|><|b (the inputs the argument actually uses).
(2) With all K4 hypotheses but one dropped (as in code/k4drop.py), in P(P_4).
Usage: python3 claimtest.py n"""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review3/code')
from fast import projections, theta, join, commute, matched, show
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
P = projections(n); t0 = time.time()
le = lambda p, q: theta(q, p) == p
def ncl(J, Y): return sum(1 for K in J if K & Y)
pairs = [(a, c) for a in P for c in P if matched(a, c)]

# (1) a|><|c|><|b only
tot = claim = ident = leftn = 0; ex = None
for a, c in pairs:
    for b in P:
        if not matched(b, c): continue
        v = theta(b, a); u = theta(a, b); tot += 1
        lhs = ncl(list(v[0]), b[1]); rhs = ncl(join(v, c), c[1]); nn = len([B for B in u[0] if B & u[1]])
        ident += (lhs == rhs); leftn += (lhs == nn); claim += (v[1] == b[1])
        if v[1] != b[1] and lhs == rhs and ex is None: ex = (a, c, b, v, lhs, rhs, nn)
print('(1) a|><|c|><|b in P(P_%d): %d triples' % (n, tot))
print('    delta\' identity |eps_v|_{supp b} = |eps_v v eps_c|_{supp c} holds in %d (as Lemma 5.40 says)' % ident)
print('    "left side is n" holds in %d;  claim supp v = supp b holds in %d' % (leftn, claim))
if ex:
    a, c, b, v, lhs, rhs, nn = ex
    print('    example with the identity true and the claim false: a=%s c=%s b=%s v=theta_b(a)=%s  lhs=%d rhs=%d n=%d' % (show(a, n), show(c, n), show(b, n), show(v, n), lhs, rhs, nn))

# (2) drop one K4 hypothesis at a time
res = {}
def bump(k, inst):
    a, b, c, y, z = inst; v = theta(b, a)
    s = res.setdefault(k, [0, 0, 0, None]); s[0] += 1
    if v[1] != b[1]:
        s[1] += 1
        if s[3] is None: s[3] = inst
    if not matched(a, b): s[2] += 1
for a, c in pairs:
    Y3 = [y for y in P if theta(a, y) == a]           # drop y~c
    Y5 = [y for y in P if commute(y, c)]              # drop theta_a(y)=a
    Y = [y for y in Y3 if commute(y, c)]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        Z4 = [z for z in P if theta(z, a) == u]                # drop b<=z
        Z7 = [z for z in P if le(b, z)]                        # drop theta_z(a)=u
        Z = [z for z in Z4 if le(b, z)]
        for z in Z:
            for y in Y:
                if theta(z, y) == v: bump('full', (a, b, c, y, z))
                else: bump('drop theta_z(y)=v', (a, b, c, y, z))
            for y in Y3:
                if theta(z, y) == v and not commute(y, c): bump('drop yc=cy', (a, b, c, y, z))
            for y in Y5:
                if theta(z, y) == v and theta(a, y) != a: bump('drop theta_a(y)=a', (a, b, c, y, z))
        for z in Z4:
            if le(b, z): continue
            for y in Y:
                if theta(z, y) == v: bump('drop b<=z', (a, b, c, y, z))
        for z in Z7:
            if theta(z, a) == u: continue
            for y in Y:
                if theta(z, y) == v: bump('drop theta_z(a)=u', (a, b, c, y, z))
    # drop c|><|b: replace b|><|c by nothing?  (b arbitrary) -- too many; instead drop a|><|c half: skip
print('(2) P_%d, one K4 hypothesis dropped (%.0fs):' % (n, time.time() - t0))
for k, (tot, bad, nab, inst) in sorted(res.items()):
    print('  %-22s instances %7d   claim supp v = supp b fails %6d   a|><|b fails %6d' % (k, tot, bad, nab))
    if inst: print('      e.g. a=%s b=%s c=%s y=%s z=%s' % tuple(show(p, n) for p in inst))
