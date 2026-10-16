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
    v = TH[b, a]; w = TH[x, a]; u = TH[a, b]; r = TH[y, a]
    TV = [B for B in P[v][0] if B & P[v][1]]; NV = [B for B in P[v][0] if not B & P[v][1]]
    TW = [B for B in P[w][0] if B & P[w][1]]; TU = [B for B in P[u][0] if B & P[u][1]]; TR = [B for B in P[r][0] if B & P[r][1]]
    Jxb = join(px, pb); Jxa = join(px, pa); Jab = join(pa, pb); Jyb = join(py, pb); Jxc = join(px, pc)
    def one(J, S): return any(K & S == S for K in J)
    S = {}
    S['TARGET th_b(x)=v'] = TH[b, x] == v
    S['(S23) each W meets <=1 T(v)-block'] = all(sum(1 for V in TV if V & W) <= 1 for W in TW)
    S['(S24) each W meets <=1 N(v)-block inside supp b'] = all(sum(1 for V in NV if V & sb and V & W) <= 1 for W in TW)
    S['(S25) each W meets <=1 T(u)-block'] = all(sum(1 for U in TU if U & W) <= 1 for W in TW)
    S['(S26) each T(v)-block meets <=1 W'] = all(sum(1 for W in TW if V & W) <= 1 for V in TV)
    S['(S27) each Y meets <=1 T(v)-block'] = all(sum(1 for V in TV if V & Y) <= 1 for Y in TY)
    S['(S28) each Y meets <=1 W'] = all(sum(1 for W in TW if W & Y) <= 1 for Y in TY)
    S['(S29) each T(r)-block meets <=1 T(v)-block'] = all(sum(1 for V in TV if V & R) <= 1 for R in TR)
    S['(S30) each T(v)-block lies in a T(r)-block'] = all(any(V & R == V for R in TR) for V in TV)
    S['(S31) each X meets <=1 T(r)-block'] = all(sum(1 for R in TR if R & X) <= 1 for X in TX)
    S['(S32) each W meets <=1 T(r)-block'] = all(sum(1 for R in TR if R & W) <= 1 for W in TW)
    S['(S33) class of a v b of a W-A meets W in supp b: W&supp b subset D_j'] = all(all((cls_of(Jab, A) & W & sb) == (W & sb) for A in TA if A & W) for W in TW)
    S['(S34) each W meets <=1 class of a v b'] = all(sum(1 for K in Jab if K & W) <= 1 for W in TW)
    S['(S35) each W meets <=1 class of a v b among those meeting supp a u supp b'] = all(sum(1 for K in Jab if K & W and K & (sa | sb)) <= 1 for W in TW)
    S['(S36) two X in one W meeting the same T(v)-block are in one class of x v b'] = all(one(Jxb, sum(X for X in TX if X & W and X & V)) for W in TW for V in TV if sum(1 for X in TX if X & W and X & V) >= 2)
    S['(S37) X in a W meets supp b or supp a'] = all((X & sb) or (X & sa) for X in TX if any(X & W == X for W in TW))
    S['(S38) every X in W meets supp y'] = all(X & sy for X in TX if any(X & W == X for W in TW))
    S['(S39) eps_x <= eps_y v eps_b'] = all(one(Jyb, X) for X in P[x][0])
    S['(S40) eps_x <= eps_y v eps_c'] = all(one(join(py, pc), X) for X in P[x][0])
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
pickle.dump(res, open('l1c_explore3_%d.pkl' % n, 'wb'))
