"""(L1c) in P(P_4): a><c><b, th_y(a)=th_z(y), th_c(z)=th_x(a), th_x(a)=th_y(x), th_z(x)=v  =>  th_b(x)=v.
All instances (numpy enumeration), structural statements, and the dropped-hypothesis map of each statement.
Usage: python3 l1c_explore.py [n]"""
import sys, time, itertools, pickle
import numpy as np
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
P = projections(n); N = len(P); idx = {p: i for i, p in enumerate(P)}
TH = np.array([[idx[theta(P[i], P[j])] for j in range(N)] for i in range(N)], dtype=np.int32)   # TH[i,j] = theta_i(j)
MT = np.array([[TH[i, j] == i and TH[j, i] == j for j in range(N)] for i in range(N)])
HYP = ['th_y(a)=th_z(y)', 'th_c(z)=th_x(a)', 'th_x(a)=th_y(x)', 'th_z(x)=v']
def instances(drop=None):
    """all (a,c,b,x,y,z) with the path and the hypotheses except `drop` (which must then FAIL)."""
    out = []
    for a in range(N):
        for c in np.nonzero(MT[a])[0]:
            for b in np.nonzero(MT[c])[0]:
                v = TH[b, a]
                # grid over (z, x)
                h2 = TH[c, :][:, None] == TH[:, a][None, :]      # th_c(z) = th_x(a)   [z, x]
                h4 = TH == v                                      # th_z(x) = v         [z, x]
                g = np.ones((N, N), dtype=bool)
                if drop != 'th_c(z)=th_x(a)': g &= h2
                if drop != 'th_z(x)=v': g &= h4
                for z, x in zip(*np.nonzero(g)):
                    if drop == 'th_c(z)=th_x(a)' and h2[z, x]: continue
                    if drop == 'th_z(x)=v' and h4[z, x]: continue
                    h1 = TH[:, a] == TH[z, :]        # th_y(a) = th_z(y)   over y
                    h3 = TH[x, a] == TH[:, x]        # th_x(a) = th_y(x)   over y
                    gy = np.ones(N, dtype=bool)
                    if drop != 'th_y(a)=th_z(y)': gy &= h1
                    else: gy &= ~h1
                    if drop != 'th_x(a)=th_y(x)': gy &= h3
                    else: gy &= ~h3
                    for y in np.nonzero(gy)[0]: out.append((a, c, b, int(x), int(y), int(z)))
    return out
def blocks(p):
    B, T = P[p]; return [bb for bb in B if bb & T], [bb for bb in B if not bb & T], T
def cls_of(J, S):
    for K in J:
        if K & S: return K
def statements(a, c, b, x, y, z):
    pa, pb, pc, px, py, pz = (P[i] for i in (a, b, c, x, y, z))
    TA, NA, sa = blocks(a); TB, NB, sb = blocks(b); TC, NC, sc = blocks(c); TX, NX, sx = blocks(x); TY, NY, sy = blocks(y); TZ, NZ, sz = blocks(z)
    v = TH[b, a]; w = TH[x, a]
    TV = [B for B in P[v][0] if B & P[v][1]]; NV = [B for B in P[v][0] if not B & P[v][1]]
    TW = [B for B in P[w][0] if B & P[w][1]]
    Jxb = join(px, pb); Jxy = join(px, py); Jxz = join(px, pz); Jyb = join(py, pb)
    def one(J, S): return any(K & S == S for K in J)
    S = {}
    S['TARGET th_b(x)=v'] = TH[b, x] == v
    S['(S2) eps_y <= eps_x v eps_b'] = all(one(Jxb, B) for B in P[y][0])
    S['(S3) each T(v)-block in one class of x v b'] = all(one(Jxb, B) for B in TV)
    S['(S4) each N(z)-block in one class of x v b'] = all(one(Jxb, B) for B in NZ)
    S['(S4b) each N(v)-block in one class of x v b'] = all(one(Jxb, B) for B in NV)
    S['(S5) class of x v b of an N(v)-block misses supp x'] = all(not (cls_of(Jxb, B) & sx) for B in NV if B & sb)
    S['(S5b) class of x v b of a T(v)-block meets supp x'] = all(cls_of(Jxb, B) & sx for B in TV)
    S['(S6) X-blocks meeting a Y lie in one class of x v b'] = all(one(Jxb, sum(X for X in TX if X & Y)) for Y in TY if any(X & Y for X in TX))
    S['(S7) X-blocks of one W lie in one class of x v b'] = all(one(Jxb, W & sx) for W in TW if W & sx)
    S['(S8) every X in a W meets supp b'] = all(X & sb for X in TX if any(X & W == X for W in TW))
    S['(S9) every X meets supp z'] = all(X & sz for X in TX)
    S['(S10) every X in a W meets supp z'] = all(X & sz for X in TX if any(X & W == X for W in TW))
    S['(S11) Y in a W lies in supp b'] = all(Y & sb == Y for Y in TY if any(Y & W == Y for W in TW))
    S['(S12) every W meets supp b'] = all(W & sb for W in TW)
    S['(S13) every W meets supp z'] = all(W & sz for W in TW)
    S['(S14) every T(v)-block meets supp x'] = all(B & sx for B in TV)
    S['(S15) eps_b <= eps_x v eps_z'] = all(one(Jxz, B) for B in P[b][0])
    S['(S16) eps_z <= eps_x v eps_b'] = all(one(Jxb, B) for B in P[z][0])
    S['(S17) X meeting supp b lies in supp z'] = all(X & sz == X for X in TX if X & sb)
    S['(S18) X meeting supp b lies in supp y'] = all(X & sy == X for X in TX if X & sb)
    S['(S19) b-blocks meeting an X: at most one T(v)-block'] = all(sum(1 for B in TV if B & X) <= 1 for X in TX)
    S['(S20) x-block meets <=1 T(v)-block'] = all(sum(1 for B in TV if B & X) <= 1 for X in P[x][0])
    S['(S21) N(x)-block meets <=1 T(v)-block'] = all(sum(1 for B in TV if B & X) <= 1 for X in NX)
    S['(S22) every T(v)-block is a union of X-blocks and N(x)-blocks? (eps_x <= on V)'] = all(all(one([B], X) for X in P[x][0] if X & B) for B in TV)
    return S
t0 = time.time(); res = {}
import os
for key in ['full'] + ['-' + h for h in HYP]:
    fn = 'l1c_inst%d_%s.npy' % (n, key.replace('(', '').replace(')', '').replace('=', '_'))
    if os.path.exists(fn): I = [tuple(int(t) for t in row) for row in np.load(fn)]
    else:
        I = instances(None if key == 'full' else key[1:]); np.save(fn, np.array(I, dtype=np.int16))
    d = res[key] = {}
    for inst in I:
        for k, val in statements(*inst).items():
            e = d.setdefault(k, [0, 0]); e[0] += 1; e[1] += (not val)
    print('%s: %d instances (%.0fs)' % (key, len(I), time.time() - t0), flush=True)
keys = list(res)
names = list(res['full'].keys())
print('%-44s' % 'statement (FAILS/instances)' + ''.join('%20s' % k for k in keys))
for s in names:
    print('%-44s' % s + ''.join('%20s' % ('%d/%d' % (res[k][s][1], res[k][s][0]) if s in res[k] else '-') for k in keys))
pickle.dump(res, open('l1c_explore2_%d.pkl' % n, 'wb'))
