"""Numerical check of the lemmas used in the state-graph proof of K4 (P_4 instances + random P_5)."""
import sys, pickle, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def cls_of(J, S):
    for K in J:
        if K & S: return K
def check(I, n):
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    u = theta(a, b); v = theta(b, a)
    Jac = join(a, c); Jbc = join(b, c); Jay = join(a, y); Jzy = join(z, y); Jyc = join(y, c); Jab = join(a, b)
    M = join((tuple(Jay), 0), z)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    TY = [B for B in y[0] if B & y[1]]; TZ = [B for B in z[0] if B & z[1]]; NZ = [B for B in z[0] if not (B & z[1])]
    rec('supp a subset supp z', a[1] & z[1] == a[1])
    rec('N(z)-blocks are a-blocks and b-blocks', all(O in a[0] and O in b[0] for O in NZ))
    rec('N(a) in supp z = union of T(z)', all(all(any(Z & P == Z for Z in TZ) or not (Z & P) for Z in TZ) for P in a[0] if not (P & a[1]) and P & z[1]))
    rec('eps_z v eps_c = eps_b v eps_c', sorted(join(z, c)) == sorted(Jbc))
    rec('eps_z v eps_y = eps_b v eps_y', sorted(Jzy) == sorted(join(b, y)))
    # Delta_i cap supp z = B_i
    for C in TC:
        D = cls_of(Jbc, C); Bi = [B for B in TB if B & D][0]
        rec('Delta_i cap supp z = B_i', D & z[1] == Bi)
    # y-block meeting N(c)-block lies inside it
    for Y in y[0]:
        for E in c[0]:
            if E & c[1]: continue
            if Y & E: rec('y-block meeting N(c) inside it', Y & ~E == 0)
    # every y-block not meeting an N(c)-block lies in union of C's
    Cun = 0
    for C in TC: Cun |= C
    for Y in y[0]:
        if not any(Y & E for E in c[0] if not (E & c[1])): rec('y-block avoiding N(c) subset union of C', Y & ~Cun == 0)
    # M_j = union of E_i, T(y) of M_j inside K'_j, D_j subset M_j, no F in M_j
    Kj_list = [K for K in join(a, z) if K & a[1]]
    for Kj in Kj_list:
        Mj = cls_of(M, Kj); Es = [cls_of(Jay, A) for A in TA if A & Kj]
        un = 0
        for E in Es: un |= E
        rec('M_j = union of E_i', Mj == un)
        Dj = cls_of(Jab, Kj); rec('D_j subset M_j', Dj & ~Mj == 0); rec('D_j subset supp z', Dj & ~z[1] == 0)
        Sj = Dj & b[1]; Kp = cls_of(Jzy, Sj); rec("K'_j cap supp z = S_j", Kp & z[1] == Sj); rec("K'_j subset M_j", Kp & ~Mj == 0)
        rec("T(y) of M_j inside K'_j", Mj & y[1] == Kp & y[1])
        # B_i subset D_j iff A_i subset K_j
        for A in TA:
            C = [C for C in TC if cls_of(Jac, A) & C][0]; Bi = [B for B in TB if cls_of(Jbc, C) & B][0]
            rec('A_i in K_j iff B_i in D_j', (A & Kj == A) == (Bi & Dj == Bi))
        # points of K'_j: gamma, lambda defined
        for x in range(n):
            if not (Kp >> x & 1): continue
            cx = [E for E in c[0] if E >> x & 1][0]
            rec("point of K'_j: c-block in some Gamma_i", bool(cls_of(Jac, cx) & a[1]))
            rec("point of K'_j: c-block in some Delta_i", bool(cls_of(Jbc, cx) & b[1]))
        # 'outer block meeting c-block E => same Delta-class' trivial; skip
    return
INST = pickle.load(open('k4inst4.pkl', 'rb'))
for I in INST: check(I, 4)
print('P_4 done');
for k, (tot, ok) in sorted(stats.items()): print('  %-44s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
# random P_5 instances
stats.clear(); P = projections(5); random.seed(3); t0 = time.time(); cnt = 0
le = lambda p, q: theta(q, p) == p
pairs = [(a, c) for a in P for c in P if matched(a, c)]; random.shuffle(pairs)
for a, c in pairs:
    if time.time() - t0 > 900: break
    Ys = [y for y in P if theta(a, y) == a and commute(y, c)]
    if not Ys: continue
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        for z in P:
            if not (le(b, z) and theta(z, a) == u): continue
            for y in Ys:
                if theta(z, y) == v:
                    check({'a': a, 'b': b, 'c': c, 'y': y, 'z': z}, 5); cnt += 1
print('P_5: %d instances (%.0fs)' % (cnt, time.time() - t0))
for k, (tot, ok) in sorted(stats.items()): print('  %-44s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
