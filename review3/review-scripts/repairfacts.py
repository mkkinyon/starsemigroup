"""Sanity check of the ingredients of the reviewer's proposed repair of Step 2 of Thm 5.49, on P(P_4) instances
with one K4 hypothesis dropped.  Each fact is tested on the instances that keep the hypotheses it is supposed to need;
a FAIL would mean that the dependency analysis in the report is wrong.
Facts:
 (Fa) [needs a|><|c, theta_z(a)=u, theta_z(c)=b]  every class of Omega = eps_a v eps_b v eps_c meeting supp c contains
      exactly one 'generalised K' (a T(u)-block K_j or an N(z)-block that is a union of T(a)-blocks), and Omega = eps_u v eps_c.
 (Fb) [needs theta_a(y)=a, theta_z(a)=u, a|><|c]  |eps_a v eps_y| - |M| = m - n - t2 and the M-classes containing the E_i
      are exactly n + t2 distinct classes, M_j = union of E_i (i in I_j), M(Z_0) = union of E_i (A_i in Z_0).
 (Fc) [needs theta_z(y)=v]  a class of eps_z v eps_y meeting supp z and supp y meets supp z in a T(v)-block; one not
      meeting supp y meets supp z in an N(v)-block or not at all.
 (Fd) [needs yc=cy]  every c-block lies in one class of eps_z v eps_y or is contained in the union of the T(y)-carrying classes.
 (Fe) [needs theta_z(a)=u]  every a-block is a z-block or lies inside supp z.
 (Ff) [needs theta_z(y)=v, theta_a(b)=u<=... ] a T(y)-free class K meeting supp z: K cap supp z lies in a single class of eps_a v eps_b.
"""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review3/code')
from fast import projections, theta, join, commute, matched, show
n = 4; P = projections(n); t0 = time.time()
le = lambda p, q: theta(q, p) == p
def cls_of(J, S):
    for K in J:
        if K & S: return K
def bT(p): return [B for B in p[0] if B & p[1]]
def bN(p): return [B for B in p[0] if not (B & p[1])]
def jm(*ps):
    cur = ps[0]
    for q in ps[1:]: cur = (tuple(join(cur, q)), 0)
    return list(cur[0])
def facts(a, b, c, y, z):
    u = theta(a, b); v = theta(b, a); F = {}
    TA = bT(a); m = len(TA); Ks = bT(u); nn = len(Ks)
    Jaz = join(a, z); Z0s = [K for K in Jaz if K & a[1] and not (K & z[1])]; t2 = len(Z0s)
    genK = Ks + Z0s
    Om = jm(a, b, c)
    F['Fa'] = sorted(Om) == sorted(join(u, c)) and all(sum(1 for K in genK if K & O) == 1 for O in Om if O & c[1])
    Jay = join(a, y); M = jm(a, z, y)
    Es = {A: cls_of(Jay, A) for A in TA}
    Mcl = {cls_of(M, A) for A in TA}
    F['Fb'] = (len(Jay) - len(M) == m - nn - t2) and len(Mcl) == nn + t2 and \
        all(cls_of(M, K) == sum({Es[A] for A in TA if A & K}) for K in genK)
    Jzy = join(z, y); TV = bT(v); NV = bN(v)
    F['Fc'] = all(((K & z[1]) in TV) if (K & y[1]) else ((K & z[1]) == 0 or (K & z[1]) in NV) for K in Jzy if K & z[1])
    Yun = sum(K for K in Jzy if K & y[1])
    F['Fd'] = all(any(E & K == E for K in Jzy) or (E & ~Yun == 0) for E in c[0])
    F['Fe'] = all(any(A & Z == A for Z in z[0]) or (A & ~z[1] == 0) for A in a[0])
    Jab = join(a, b)
    F['Ff'] = all(any((K & z[1]) & D == (K & z[1]) for D in Jab) for K in Jzy if (K & z[1]) and not (K & y[1]))
    return F
needs = {'Fa': {'theta_z(a)=u', 'b<=z', 'theta_z(y)=v', 'yc=cy'}, 'Fb': {'theta_a(y)=a', 'theta_z(a)=u'}, 'Fc': {'theta_z(y)=v'},
         'Fd': {'yc=cy'}, 'Fe': {'theta_z(a)=u'}, 'Ff': {'theta_z(y)=v'}}
res = {}
def bump(dropped, inst):
    F = facts(*inst)
    for name, val in F.items():
        key = (dropped, name, dropped in needs[name])
        s = res.setdefault(key, [0, 0]); s[0] += 1; s[1] += bool(val)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
for a, c in pairs:
    Y3 = [y for y in P if theta(a, y) == a]; Y5 = [y for y in P if commute(y, c)]; Y = [y for y in Y3 if commute(y, c)]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        Z4 = [z for z in P if theta(z, a) == u]; Z7 = [z for z in P if le(b, z)]; Z = [z for z in Z4 if le(b, z)]
        for z in Z:
            for y in Y:
                if theta(z, y) == v: bump('none', (a, b, c, y, z))
                else: bump('theta_z(y)=v', (a, b, c, y, z))
            for y in Y3:
                if theta(z, y) == v and not commute(y, c): bump('yc=cy', (a, b, c, y, z))
            for y in Y5:
                if theta(z, y) == v and theta(a, y) != a: bump('theta_a(y)=a', (a, b, c, y, z))
        for z in Z4:
            if le(b, z): continue
            for y in Y:
                if theta(z, y) == v: bump('b<=z', (a, b, c, y, z))
        for z in Z7:
            if theta(z, a) == u: continue
            for y in Y:
                if theta(z, y) == v: bump('theta_z(a)=u', (a, b, c, y, z))
print('P_4 (%.0fs).  fact / dropped hypothesis / (does the fact need it?) : holds/total' % (time.time() - t0))
for (dropped, name, needed), (tot, ok) in sorted(res.items(), key=lambda kv: (kv[0][1], kv[0][0])):
    flag = '' if ok == tot else ('   (fails, but needs the dropped hypothesis: fine)' if needed else '   *** FAILS WITHOUT NEEDING THE DROPPED HYPOTHESIS ***')
    print('  %s  dropped=%-14s needed=%-5s %7d/%-7d%s' % (name, dropped, needed, ok, tot, flag))
