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
    Jac = join(a, c); Jbc = join(b, c); Jay = join(a, y); Jzy = join(z, y); Jab = join(a, b); Jzc = join(z, c)
    TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
    Es = [cls_of(Jay, A) for A in TA]
    trip = []
    for A in TA:
        C = [C for C in TC if cls_of(Jac, A) & C][0]; Bi = [B for B in TB if cls_of(Jbc, C) & B][0]
        trip.append((A, C, Bi, cls_of(Jay, A), cls_of(Jac, A), cls_of(Jbc, C), cls_of(Jab, A), cls_of(Jzy, Bi)))
    for k, (A, C, Bi, E, G, Dl, D, Kp) in enumerate(trip):
        others = 0
        for k2, t2 in enumerate(trip):
            if k2 != k: others |= t2[3]
        rec('Delta_i cap E_k = 0 (k!=i)', Dl & others == 0)
        rec('Gamma_i cap E_k = 0 (k!=i)', G & others == 0)
        rec('Delta_i cap supp y subset E_i', Dl & y[1] & ~E == 0)
        rec('Gamma_i cap supp y subset E_i', G & y[1] & ~E == 0)
        rec('Delta_i subset E_i', Dl & ~E == 0)
        rec('Gamma_i subset E_i', G & ~E == 0)
        rec("K'_j cap E_k = 0 (k!=i)", Kp & others == 0)
        rec("K'_j subset E_i", Kp & ~E == 0)
        rec("C_i subset E_i", C & ~E == 0)
        rec("B_i subset E_i", Bi & ~E == 0)
        rec("Delta_i cap supp z (=B_i) subset E_i", Dl & z[1] & ~E == 0)
        rec("E_i cap supp c subset C_i", E & c[1] & ~C == 0)
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): print('  %-44s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
