"""K4 reconnaissance III: c-block indices.  For each c-block E: index i with E in Gamma_i (if any), j with E in Delta_j (if any)."""
import sys, pickle
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 4; P = projections(n)
INST = pickle.load(open('k4inst4.pkl', 'rb'))
def cls_of(J, S):
    for K in J:
        if K & S: return K
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def rk_prod(p, q): return sum(1 for K in join(p, q) if K & p[1] and K & q[1])
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    Jac = join(a, c); Jbc = join(b, c); Jab = join(a, b); Jay = join(a, y); Jyc = join(y, c); Jzc = join(z, c); Jzy = join(z, y)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    TY = [B for B in y[0] if B & y[1]]; TZ = [B for B in z[0] if B & z[1]]
    m = len(TA)
    idxG = {}; idxD = {}
    for k, C in enumerate(TC):
        idxG[cls_of(Jac, C)] = k; idxD[cls_of(Jbc, C)] = k
    for E in c[0]:
        gi = idxG.get(cls_of(Jac, E)); dj = idxD.get(cls_of(Jbc, E))
        if gi is not None and dj is not None:
            rec('c-block in Gamma_i & Delta_j => i=j', gi == dj)
            if not (E & c[1]): rec('N(c)-block in Gamma_i & Delta_j => i=j', gi == dj)
        if gi is not None and dj is None: rec('c-block in Gamma_i, in no Delta', 1)
        if gi is None and dj is not None: rec('c-block in Delta_j, in no Gamma', 1)
    w = theta(y, c)
    rec('theta_a(yc)=a', theta(a, w) == a)
    rec('rk(yc)=m', rk_prod(y, c) == m)
    rec('theta_b(yc)=b', theta(b, w) == b)
    for Y in y[0]:
        rec('y-block meets <=1 B', sum(1 for B in TB if B & Y) <= 1)
        rec('y-block meets <=1 C', sum(1 for C in TC if C & Y) <= 1)
    for Z in TZ:
        rec('T(z)-block meets <=1 C', sum(1 for C in TC if C & Z) <= 1)
        rec('T(z)-block meets <=1 A', sum(1 for A in TA if A & Z) <= 1)
    for E in c[0]:
        if E & c[1]: continue
        rec('N(c)-block meets <=1 T(z)', sum(1 for Z in TZ if E & Z) <= 1)
        rec('N(c)-block meets supp a => meets supp b', (not (E & a[1])) or bool(E & b[1]))
        rec('N(c)-block meets supp b => meets supp a', (not (E & b[1])) or bool(E & a[1]))
        rec('N(c)-block meets supp a => meets supp z', (not (E & a[1])) or bool(E & z[1]))
        rec('N(c)-block meets supp z => meets supp b', (not (E & z[1])) or bool(E & b[1]))
print(len(INST), 'instances')
for k, (tot, ok) in stats.items(): print('  %-48s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
