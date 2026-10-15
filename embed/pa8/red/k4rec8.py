import sys, pickle
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def cls_of(J, S):
    for K in J:
        if K & S: return K
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    Jac = join(a, c); Jbc = join(b, c); Jay = join(a, y); Jzy = join(z, y); Jab = join(a, b)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    trip = []
    for A in TA:
        C = [C for C in TC if cls_of(Jac, A) & C][0]; Bi = [B for B in TB if cls_of(Jbc, C) & B][0]
        trip.append((A, C, Bi, cls_of(Jay, A), cls_of(Jab, A)))
    for Y in y[0]:
        isT = bool(Y & y[1])
        for (A, C, Bi, E, D) in trip:
            if Y & C & Bi:
                rec('Y meets C_i&B_i => Y in E_i', Y & ~E == 0)
                rec('Y meets C_i&B_i => Y in E_i  [T(y)]' if isT else 'Y meets C_i&B_i => Y in E_i  [N(y)]', Y & ~E == 0)
                rec('Y meets C_i&B_i => Y in D_j', Y & ~D == 0)
                rec('Y meets C_i&B_i => Y meets A_i', bool(Y & A))
            if Y & C:
                rec('Y meets C_i => Y in E_i', Y & ~E == 0)
                rec('Y meets C_i => Y meets supp a', bool(Y & a[1]))
            if Y & Bi:
                rec('Y meets B_i => Y in E_i', Y & ~E == 0)
                rec('Y meets B_i => Y in D_j', Y & ~D == 0)
                rec('Y meets B_i => Y meets A_i', bool(Y & A))
                rec('Y meets B_i => Y meets C_i', bool(Y & C))
            if Y & A:
                rec('Y meets A_i => Y meets B_i', bool(Y & Bi))
                rec('Y meets A_i => Y meets C_i', bool(Y & C))
                rec('Y meets A_i => Y meets supp b', bool(Y & b[1]))
                rec('Y meets A_i => Y meets supp z', bool(Y & z[1]))
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): print('  %-44s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
