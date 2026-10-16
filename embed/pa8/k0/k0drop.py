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
    u = theta(a, b); v = theta(b, a); p = theta(z, a); s = theta(z, y); t = theta(z, c); w = theta(y, c)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]
    Jay = join(a, y); Jby = join(b, y)
    S = {}
    S['a><b'] = matched(a, b)
    S['a<=y'] = theta(y, a) == a
    S['every A meets supp y'] = all(A & y[1] for A in TA)
    S['no class of a v y has two A'] = all(sum(1 for A in TA if A & K) <= 1 for K in Jay)
    S['every B meets supp y'] = all(B & y[1] for B in TB)
    S['no class of b v y has two B'] = all(sum(1 for B in TB if B & K) <= 1 for K in Jby)
    S['s=p (th_z(y)=th_z(a))'] = s == p
    S['t=p (th_z(c)=th_z(a))'] = t == p
    S['th_y(p)=u'] = theta(y, p) == u
    S['y~p'] = commute(y, p)
    S['y~a'] = commute(y, a); S['y~b'] = commute(y, b)
    S['a><p'] = matched(a, p); S['b><p'] = matched(b, p)
    S['u=ya'] = u == theta(y, a); S['v=yb'] = v == theta(y, b)
    S['c<=y'] = theta(y, c) == c
    S['s<=p'] = theta(p, s) == s
    S['u><s'] = matched(u, s)
    S['supp a subset supp y'] = a[1] & y[1] == a[1]
    S['supp c subset supp y'] = c[1] & y[1] == c[1]
    S['th_c(z)=c'] = theta(c, z) == c
    S['th_a(z)=a'] = theta(a, z) == a
    S['z~p'] = commute(z, p)
    S['eps_a v eps_z = eps_a v eps_p'] = sorted(join(a, z)) == sorted(join(a, p))
    S['th_w(z)=w'] = theta(w, z) == w
    S['th_p(y)=p'] = theta(p, y) == p
    S['th_y(c)=th_y(z)'] = theta(y, c) == theta(y, z)
    S['A_i and B_i in same class of a v b... (closing)'] = None
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
