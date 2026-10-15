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
    Jac = join(a, c); Jbc = join(b, c); Jay = join(a, y); Jzy = join(z, y)
    TA = [B for B in a[0] if B & a[1]]; TC = [B for B in c[0] if B & c[1]]; TB = [B for B in b[0] if B & b[1]]
    trip = []
    for A in TA:
        C = [C for C in TC if cls_of(Jac, A) & C][0]; Bi = [B for B in TB if cls_of(Jbc, C) & B][0]
        trip.append((A, C, Bi))
    # a-blocks adjacent to C_p (meeting C_p): their E-classes
    adjE = []; adjEB = []; adjEY = []
    for (A, C, Bi) in trip:
        s = set(); sB = set(); sY = set()
        for P in a[0]:
            if P & C:
                s.add(cls_of(Jay, P))
                if P & C & Bi: sB.add(cls_of(Jay, P))
                if P & C & Bi & y[1]: sY.add(cls_of(Jay, P))
        adjE.append(s); adjEB.append(sB); adjEY.append(sY)
    for p in range(len(trip)):
        for q in range(p + 1, len(trip)):
            rec('a-blocks adj to C_p, C_q in different E-classes', not (adjE[p] & adjE[q]))
            rec('a-blocks at C_p&B_p, C_q&B_q in different E-classes', not (adjEB[p] & adjEB[q]))
            rec('a-blocks at C_p&B_p&supp y, C_q&B_q&supp y different E', not (adjEY[p] & adjEY[q]))
print(len(INST), 'instances')
for k, (tot, ok) in sorted(stats.items()): print('  %-56s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
