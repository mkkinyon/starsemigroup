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
    S = {}
    S['TARGET th_b(x)=v'] = TH[b, x] == v
    S['th_x(b)=w'] = TH[x, b] == w
    S['a><b'] = MT[a, b]
    def refines(q, J): return all(any(K & B == B for K in J) for B in P[q][0])
    def refT(q, J): return all(any(K & B == B for K in J) for B in P[q][0] if B & P[q][1])
    Jxa = join(px, pa); Jxc = join(px, pc); Jxb = join(px, pb); Jyb = join(py, pb); Jyx = join(py, px); Jzb = join(pz, pb); Jab = join(pa, pb); Jyz = join(py, pz); Jxy = join(px, py); Jya = join(py, pa); Jcb = join(pc, pb)
    for nm, T_, s_ in [('A', TA, 'a'), ('B', TB, 'b'), ('C', TC, 'c')]:
        for nm2, s2 in [('x', sx), ('y', sy), ('z', sz)]:
            S['every %s meets supp %s' % (nm, nm2)] = all(B & s2 for B in T_)
    S['every X meets supp b'] = all(B & sb for B in TX); S['every X meets supp a'] = all(B & sa for B in TX); S['every X meets supp c'] = all(B & sc for B in TX)
    S['every Y meets supp b'] = all(B & sb for B in TY); S['every Z meets supp b'] = all(B & sb for B in TZ)
    S['eps_c <= eps_x v eps_a'] = refines(c, Jxa); S['eps_a <= eps_x v eps_c'] = refines(a, Jxc)
    S['eps_b <= eps_x v eps_a'] = refines(b, Jxa); S['eps_b <= eps_x v eps_y'] = refines(b, Jxy); S['eps_b <= eps_x v eps_c'] = refines(b, Jxc)
    S['eps_x <= eps_y v eps_b'] = refines(x, Jyb); S['eps_x <= eps_a v eps_b'] = refines(x, Jab); S['eps_x <= eps_c v eps_b'] = refines(x, Jcb)
    S['eps_a <= eps_x v eps_b'] = refines(a, Jxb); S['eps_c <= eps_x v eps_b'] = refines(c, Jxb)
    S['eps_z <= eps_x v eps_b'] = refines(z, Jxb); S['eps_y <= eps_x v eps_b'] = refines(y, Jxb)
    S['T(x) meets <=1 B'] = all(sum(1 for B in TB if B & X) <= 1 for X in TX)
    S['T(x) meets <=1 A'] = all(sum(1 for B in TA if B & X) <= 1 for X in TX)
    S['T(x) meets <=1 C'] = all(sum(1 for B in TC if B & X) <= 1 for X in TX)
    S['T(y) meets <=1 B'] = all(sum(1 for B in TB if B & X) <= 1 for X in TY)
    S['T(y) meets <=1 A'] = all(sum(1 for B in TA if B & X) <= 1 for X in TY)
    S['T(z) meets <=1 B'] = all(sum(1 for B in TB if B & X) <= 1 for X in TZ)
    S['T(b) meets <=1 X'] = all(sum(1 for X in TX if B & X) <= 1 for B in TB)
    S['N(x)-block meets <=1 B'] = all(sum(1 for B in TB if B & X) <= 1 for X in NX)
    S['N(y)-block meets <=1 B'] = all(sum(1 for B in TB if B & X) <= 1 for X in NY)
    S['class of x v b with a B meets supp x'] = all((not K & sb) or (K & sx) for K in Jxb)
    S['class of x v b with an X meets supp b'] = all((not K & sx) or (K & sb) for K in Jxb)
    S['no class of x v b has two B'] = all(sum(1 for B in TB if B & K) <= 1 for K in Jxb)
    S['no class of x v a has two A'] = all(sum(1 for B in TA if B & K) <= 1 for K in Jxa)
    S['no class of y v b has two B'] = all(sum(1 for B in TB if B & K) <= 1 for K in Jyb)
    S['x~b'] = TH[x, b] == TH[b, x]
    S['supp b subset supp y'] = sb & sy == sb; S['supp x subset supp y'] = sx & sy == sx; S['supp b subset supp z'] = sb & sz == sb
    S['supp a subset supp x'] = sa & sx == sa; S['supp c subset supp x'] = sc & sx == sc; S['supp x subset supp c'] = sx & sc == sx
    S['N(b)-blocks are N(y)-blocks'] = all(B in NY for B in NB); S['N(y) subset N(b)'] = all(B in NB for B in NY)
    S['N(x) subset N(c)'] = all(B in NC for B in NX); S['N(c) subset N(x)'] = all(B in NX for B in NC)
    S['N(x) subset N(y)'] = all(B in NY for B in NX); S['N(y) subset N(x)'] = all(B in NX for B in NY)
    return S
t0 = time.time(); res = {}
for key in ['full'] + ['-' + h for h in HYP]:
    I = instances(None if key == 'full' else key[1:])
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
pickle.dump(res, open('l1c_explore%d.pkl' % n, 'wb'))
