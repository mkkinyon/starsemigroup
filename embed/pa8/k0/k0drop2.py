"""Dropped-hypothesis map for K0 in P(P_4): for each hypothesis h, instances with all but h; statements tested."""
import sys, time, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
P = projections(4)
def cls_of(J, S):
    for K in J:
        if K & S: return K
HYP = ['y~c', 'th_y(b)=v', 'th_b(z)=b', 'th_z(a)=th_z(b)', 'th_y(z)=u']
def hyps(a, b, c, y, z):
    u = theta(a, b); v = theta(b, a)
    return [commute(y, c), theta(y, b) == v, theta(b, z) == b, theta(z, a) == theta(z, b), theta(y, z) == u]
def statements(a, b, c, y, z):
    u = theta(a, b); v = theta(b, a); p = theta(z, a); s = theta(z, y); w = theta(y, c)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    TY = [B for B in y[0] if B & y[1]]; TP = [B for B in p[0] if B & p[1]]; TZ = [B for B in z[0] if B & z[1]]
    Jay = join(a, y); Jby = join(b, y); Jyz = join(y, z); Jaz = join(a, z); Jbz = join(b, z); Jcy = join(c, y)
    def refines(q, J): return all(any(K & B == B for K in J) for B in q[0])
    def refT(q, J): return all(any(K & B == B for K in J) for B in q[0] if B & q[1])
    S = {}
    S['a><b'] = matched(a, b)
    S['every A meets supp y'] = all(A & y[1] for A in TA)
    S['no class of a v y has two A'] = all(sum(1 for A in TA if A & K) <= 1 for K in Jay)
    S['eps_a <= eps_y v eps_z'] = refines(a, Jyz)
    S['eps_b <= eps_y v eps_z'] = refines(b, Jyz)
    S['eps_c <= eps_y v eps_z'] = refines(c, Jyz)
    S['eps_a <= eps_b v eps_z'] = refines(a, Jbz)
    S['eps_b <= eps_a v eps_z'] = refines(b, Jaz)
    S['eps_c <= eps_a v eps_z'] = refines(c, Jaz)
    S['eps_c <= eps_b v eps_z'] = refines(c, Jbz)
    S['eps_z <= eps_a v eps_y'] = refines(z, Jay)
    S['eps_z <= eps_b v eps_y'] = refines(z, Jby)
    S['eps_z <= eps_c v eps_y'] = refines(z, Jcy)
    S['T(z) in one class of a v y'] = refT(z, Jay)
    S['eps_p <= eps_a v eps_y'] = refines(p, Jay)
    S['eps_p <= eps_b v eps_y'] = refines(p, Jby)
    S['T(y) meets <=1 A'] = all(sum(1 for A in TA if A & H) <= 1 for H in TY)
    S['T(y) meets <=1 B'] = all(sum(1 for B in TB if B & H) <= 1 for H in TY)
    S['T(y) meets <=1 P'] = all(sum(1 for Q in TP if Q & H) <= 1 for H in TY)
    S['T(z) meets <=1 A'] = all(sum(1 for A in TA if A & Z) <= 1 for Z in TZ)
    S['every P meets supp y'] = all(Q & y[1] for Q in TP)
    S['every B meets supp y'] = all(B & y[1] for B in TB)
    S['every C meets supp y'] = all(C & y[1] for C in TC)
    S['c><p'] = matched(c, p); S['th_c(p)=c'] = theta(c, p) == c; S['th_p(c)=p'] = theta(p, c) == p
    S['y~p'] = commute(y, p); S['th_y(p)=u'] = theta(y, p) == u
    S['s<=p'] = theta(p, s) == s; S['th_s(p)=s'] = theta(s, p) == s
    S['class of y v z meeting supp z meets supp y'] = all((not (K & z[1])) or (K & y[1]) for K in Jyz)
    S['class of y v z meeting supp p meets supp y'] = all((not (K & p[1])) or (K & y[1]) for K in Jyz)
    S['A_i meets P_i'] = all(any(Q & A for Q in TP if cls_of(Jaz, A) & Q) for A in TA)
    S['th_c(z)=c'] = theta(c, z) == c
    S['th_z(c)=p'] = theta(z, c) == p
    S['supp c subset supp y'] = c[1] & y[1] == c[1]
    return S
res = {}
t0 = time.time()
pairs = [(a, c) for a in P for c in P if matched(a, c)]
def add(key, S):
    d = res.setdefault(key, {})
    for k, val in S.items():
        if val is None: continue
        e = d.setdefault(k, [0, 0]); e[0] += 1; e[1] += (not val)
for a, c in pairs:
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
print('(%.0fs) entries: FAILS/instances' % (time.time() - t0))
keys = ['full'] + ['-' + h for h in HYP]
names = list(next(iter(res.values())).keys())
print('%-44s' % 'statement' + ''.join('%18s' % k for k in keys))
for nm in names:
    print('%-44s' % nm + ''.join('%18s' % ('%d/%d' % (res[k][nm][1], res[k][nm][0]) if k in res and nm in res[k] else '-') for k in keys))
