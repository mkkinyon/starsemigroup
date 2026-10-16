"""Dropped-hypothesis map for the claims of the K0 proof (16 Oct), P(P_n). Usage: python3 k0claims.py [n] [budget]"""
import sys, time, itertools, pickle
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n)
def cls_of(J, S):
    for K in J:
        if K & S: return K
def one_class(J, S):  # S inside a single class of J
    return any(K & S == S for K in J)
HYP = ['y~c', 'th_y(b)=v', 'th_b(z)=b', 'th_z(a)=th_z(b)', 'th_y(z)=u']
def statements(a, b, c, y, z):
    u = theta(a, b); v = theta(b, a)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    TY = [B for B in y[0] if B & y[1]]; NY = [B for B in y[0] if not B & y[1]]
    Jac = join(a, c); Jbc = join(b, c); Jaz = join(a, z); Jbz = join(b, z); Jyz = join(y, z); Jay = join(a, y)
    # c-matching A_i -> C_i -> B_i
    match = {}
    for A in TA:
        G = cls_of(Jac, A); Cs = [C for C in TC if C & G]
        if len(Cs) != 1: match = None; break
        D = cls_of(Jbc, Cs[0]); Bs = [B for B in TB if B & D]
        if len(Bs) != 1: match = None; break
        match[A] = (Cs[0], Bs[0])
    S = {}
    S['a><b'] = matched(a, b)
    S['th_a(z)=a'] = theta(a, z) == a
    S['N(y)-blocks are N(a),N(b),N(c)-blocks'] = all(N in a[0] and N in b[0] and N in c[0] for N in NY)
    if match is None:
        return S
    crossing = [Y for Y in TY if sum(1 for A in TA if A & Y) >= 2]
    noncross = [Y for Y in TY if Y not in crossing]
    S['crossing Y in U(A_i&B_i&C_i)'] = all(Y & ~sum(A & match[A][0] & match[A][1] for A in TA) == 0 for Y in crossing)
    cells = [L & Lp for L in Jaz for Lp in Jbz if L & Lp]
    S['noncrossing Y in one cell'] = all(one_class(cells, Y) for Y in noncross)
    S['N(y)-block in one cell'] = all(one_class(cells, N) for N in NY)
    diag = 0
    for A in TA: diag |= cls_of(Jaz, A) & cls_of(Jbz, match[A][1])   # OR, not sum: the D_i may coincide when th_a(z)=a fails
    S['class of y v z: one cell or in diagonal cells'] = all(one_class(cells, K) or K & ~diag == 0 for K in Jyz)
    S['A_i in Lp-class of B_i'] = all(cls_of(Jbz, match[A][1]) & A == A for A in TA)
    S['eps_a <= eps_b v eps_z'] = all(one_class(Jbz, B) for B in a[0])
    S['eps_a v eps_b <= eps_b v eps_z'] = all(one_class(Jbz, K) for K in join(a, b))
    S['class of y v z with crossing Y has >=2 A'] = all(sum(1 for A in TA if A & K) >= 2 for K in Jyz if any(Y & K for Y in crossing))
    return S
res = {}
t0 = time.time()
import random; random.seed(1)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
def add(key, S):
    d = res.setdefault(key, {})
    for k, val in S.items():
        e = d.setdefault(k, [0, 0]); e[0] += 1; e[1] += (not val)
npairs = 0
for a, c in pairs:
    if time.time() - t0 > budget: break
    npairs += 1
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        Yc = {y: (commute(y, c), theta(y, b) == v) for y in P}
        Zc = {z: (theta(b, z) == b, theta(z, a) == theta(z, b)) for z in P}
        Y0 = [y for y in P if all(Yc[y])]; Y1 = [y for y in P if Yc[y].count(False) == 1]
        Z0 = [z for z in P if all(Zc[z])]; Z1 = [z for z in P if Zc[z].count(False) == 1]
        for y in Y0:
            for z in Z0:
                ok5 = theta(y, z) == u
                add('full' if ok5 else '-th_y(z)=u', statements(a, b, c, y, z))
            for z in Z1:
                if theta(y, z) == u: add('-th_b(z)=b' if not Zc[z][0] else '-th_z(a)=th_z(b)', statements(a, b, c, y, z))
        for y in Y1:
            for z in Z0:
                if theta(y, z) == u: add('-y~c' if not Yc[y][0] else '-th_y(b)=v', statements(a, b, c, y, z))
print('P_%d, %d of %d (a,c) pairs, (%.0fs) entries: FAILS/instances' % (n, npairs, len(pairs), time.time() - t0))
keys = ['full'] + ['-' + h for h in HYP]
names = list(res['full'].keys())
print('%-50s' % 'statement' + ''.join('%18s' % k for k in keys))
for s in names:
    print('%-50s' % s + ''.join('%18s' % ('%d/%d' % (res[k][s][1], res[k][s][0]) if k in res and s in res[k] else '-') for k in keys))
