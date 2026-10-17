"""Evaluate block statements on (L1c) core instances in P(P_n) (npy file), full hypotheses only. Usage: python3 l1c_stm5.py file.npy n"""
import sys, numpy as np, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
fn = sys.argv[1]; n = int(sys.argv[2])
P = projections(n); idx = {p: i for i, p in enumerate(P)}; N = len(P)
TH = np.array([[idx[theta(P[i], P[j])] for j in range(N)] for i in range(N)], dtype=np.int32)
I = np.load(fn)
def blocks(p):
    B, T = P[p]; return [b for b in B if b & T], [b for b in B if not b & T], T
def cls_of(J, S):
    for K in J:
        if K & S: return K
def one(J, S): return any(K & S == S for K in J)
def statements(a, c, b, x, y, z):
    pa, pb, pc, px, py, pz = (P[i] for i in (a, b, c, x, y, z))
    TA, NA, sa = blocks(a); TB, NB, sb = blocks(b); TC, NC, sc = blocks(c); TX, NX, sx = blocks(x); TY, NY, sy = blocks(y); TZ, NZ, sz = blocks(z)
    v = TH[b, a]; w = TH[x, a]; u = TH[a, b]; r = TH[y, a]
    TV, NV, _ = blocks(v); TW, NW, _ = blocks(w); TR, NR, _ = blocks(r); TU, NU, _ = blocks(u)
    Jxb = join(px, pb); Jxc = join(px, pc); Jxa = join(px, pa); Jyb = join(py, pb); Jzx = join(pz, px); Jab = join(pa, pb); Jcb = join(pc, pb); Jac = join(pa, pc); Jyz = join(py, pz)
    S = {}
    S['TARGET th_b(x)=v'] = TH[b, x] == v
    S['a><b'] = matched(pa, pb)
    S['(Z1) each T(z)-block in one class of x v b'] = all(one(Jxb, Z) for Z in TZ)
    S['(Z2) each T(z)-block meets <=1 B'] = all(sum(1 for B in TB if B & Z) <= 1 for Z in TZ)
    S['(Z3) each T(z)-block in one class of c v b'] = all(one(Jcb, Z) for Z in TZ)
    S['(Z4) T(z) meeting B1,B2: B1,B2 share an X'] = all(all(any(X & B1 and X & B2 for X in TX) for B1 in TB for B2 in TB if B1 < B2 and B1 & Z and B2 & Z) for Z in TZ)
    S['(Z5) eps_z <= eps_x v eps_c'] = all(one(Jxc, Z) for Z in pz[0])
    S['(Z6) eps_z <= eps_y v eps_b'] = all(one(Jyb, Z) for Z in pz[0])
    S['(Z7) eps_z <= eps_w'] = all(one(P[w][0], Z) for Z in pz[0])
    S['(Z8) eps_z <= eps_x v eps_a'] = all(one(Jxa, Z) for Z in pz[0])
    S['(Z9) eps_z <= eps_a v eps_b'] = all(one(Jab, Z) for Z in pz[0])
    S['(Z10) eps_y <= eps_x v eps_b'] = all(one(Jxb, Y) for Y in py[0])
    S['(Z11) each T(z)-block meets <=1 X'] = all(sum(1 for X in TX if X & Z) <= 1 for Z in TZ)
    S['(Z12) each X meets <=1 T(z)-block'] = all(sum(1 for Z in TZ if X & Z) <= 1 for X in TX)
    S['(Z13) each T(z) in one class of a v c'] = all(one(Jac, Z) for Z in TZ)
    S['(Z14) each T(y)-block meets <=1 B'] = all(sum(1 for B in TB if B & Y) <= 1 for Y in TY)
    S['(Z15) each T(y)-block in one Delta or T-less class of c v b'] = all(one(Jcb, Y) for Y in TY)
    S['(Z16) T(y) meeting B1,B2: B1,B2 share an X'] = all(all(any(X & B1 and X & B2 for X in TX) for B1 in TB for B2 in TB if B1 < B2 and B1 & Y and B2 & Y) for Y in TY)
    S['(Z17) two X of one W share a b-block'] = all(all(any(B & X1 and B & X2 for B in pb[0]) for X1 in TX for X2 in TX if X1 < X2 and X1 & W and X2 & W) for W in TW)
    S['(Z18) two X of one W share a c-block'] = all(all(any(B & X1 and B & X2 for B in pc[0]) for X1 in TX for X2 in TX if X1 < X2 and X1 & W and X2 & W) for W in TW)
    S['(Z19) eps_x <= eps_z v eps_b'] = all(one(join(pz, pb), X) for X in px[0])
    S['(Z20) eps_x <= eps_y v eps_b'] = all(one(Jyb, X) for X in px[0])
    S['(Z21) each X meets <=1 T(v)-block'] = all(sum(1 for V in TV if V & X) <= 1 for X in TX)
    S['(Z22) each W meets <=1 T(v)-block'] = all(sum(1 for V in TV if V & W) <= 1 for W in TW)
    S['(Z23) eps_b <= eps_z v eps_x'] = all(one(Jzx, B) for B in pb[0])
    S['(Z24) each N(v)-block in one class of x v b'] = all(one(Jxb, B) for B in NV)
    S['(Z25) class of x v b of an N(v)-block misses supp x'] = all(not (cls_of(Jxb, B) & sx) for B in NV if B & sb)
    S['(Z26) every T(v)-block class meets supp x'] = all(cls_of(Jxb, B) & sx for B in TV)
    S['(Z27) eps_c <= eps_x v eps_a'] = all(one(Jxa, C) for C in pc[0])
    S['(Z28) eps_b <= eps_x v eps_a'] = all(one(Jxa, B) for B in pb[0])
    S['(Z29) each W meets <=1 T(r)-block'] = all(sum(1 for R in TR if R & W) <= 1 for W in TW)
    S['(Z30) T(z) meeting B1,B2 (B1,B2 in V): share a Y'] = all(all(any(Y & B1 and Y & B2 for Y in TY) for B1 in TB for B2 in TB if B1 < B2 and B1 & Z and B2 & Z) for Z in TZ)
    S['(Z31) each T(z) lies in one T(r)-block'] = all(any(Z & R == Z for R in TR) for Z in TZ)
    S['(Z32) each T(v) lies in one T(r)-block'] = all(any(V & R == V for R in TR) for V in TV)
    return S
t0 = time.time(); res = {}; nd = 0
for row in I:
    inst = tuple(int(t) for t in row)
    if matched(P[inst[0]], P[inst[2]]): continue
    nd += 1
    for k, val in statements(*inst).items():
        e = res.setdefault(k, [0, 0]); e[0] += 1; e[1] += (not val)
print('%s: %d instances with a not>< b (%.0fs)' % (fn, nd, time.time() - t0))
for k, (tot, f) in res.items(): print('  %-62s FAILS %d/%d' % (k, f, tot))
