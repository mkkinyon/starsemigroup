import sys, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 4; P = projections(n); FULL = (1 << n) - 1
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def cls_of(J, S):
    for K in J:
        if K & S: return K
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    Jac = join(a, c); Jbc = join(b, c); Jab = join(a, b); Jay = join(a, y); Jyc = join(y, c); Jzy = join(z, y); Jby=join(b,y)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    TY = [B for B in y[0] if B & y[1]]; TZ = [B for B in z[0] if B & z[1]]; NY = [B for B in y[0] if not (B & y[1])]
    Nb_in_z = 0
    for B in b[0]:
        if not (B & b[1]) and B & z[1] == B: Nb_in_z |= B
    for A in TA:
        C = [C for C in TC if cls_of(Jac, A) & C][0]; Bi = [B for B in TB if cls_of(Jbc, C) & B][0]
        D = cls_of(Jab, A); E = cls_of(Jay, A)
        rec('E_i cap supp z subset D_j', E & z[1] & ~D == 0)
        rec('E_i cap supp b subset S_j', E & b[1] & ~D == 0)
        rec('E_i cap supp b subset B_i', E & b[1] & ~Bi == 0)
        rec('E_i cap supp z subset B_i u Nb', E & z[1] & ~(Bi | Nb_in_z) == 0)
        rec('E_i cap supp z subset A_i u B_i u Nb', E & z[1] & ~(Bi | Nb_in_z | A) == 0)
        rec('E_i subset D_j', E & ~D == 0)
        rec('E_i cap supp c subset C_i', E & c[1] & ~C == 0)
        rec('E_i meets C_i', bool(E & C))
        rec('E_i cap supp y subset cls_zy(B_i)', E & y[1] & ~cls_of(Jzy, Bi) == 0)
        for H in TY:
            if H & E:
                rec('T(y) in E_i: H cap supp z subset B_i', H & z[1] & ~Bi == 0)
                rec('T(y) in E_i: H meets B_i', bool(H & Bi))
                rec('T(y) in E_i: H meets supp z', bool(H & z[1]))
                rec('T(y) in E_i: H meets A_i', bool(H & A))
        for Y in NY:
            if Y & E:
                rec('N(y) in E_i: Y cap supp z subset A_i u B_i u Nb', Y & z[1] & ~(Bi | Nb_in_z | A) == 0)
        rec('A_i cap supp y subset B_i', A & y[1] & ~Bi == 0)
        rec('A_i cap supp b subset B_i', A & b[1] & ~Bi == 0)
    for Z in TZ:
        rec('T(z) inside one E-class or disjoint from supp y-classes..', sum(1 for K in Jay if K & Z) <= 1)
        rec('T(z) meeting supp a lies in supp y', (not (Z & a[1])) or Z & y[1] == Z)
        rec('T(z) meeting supp a meets supp y', (not (Z & a[1])) or bool(Z & y[1]))
        rec('T(z) in supp b lies in one y-block or in supp y', (not (Z & b[1] == Z)) or Z & y[1] == Z or any(Y & Z == Z for Y in y[0]))
        rec('T(z) lies in one y-block or in supp y', Z & y[1] == Z or any(Y & Z == Z for Y in y[0]))
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): print('  %-52s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
