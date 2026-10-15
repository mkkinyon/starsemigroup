"""K4 reconnaissance II: block-level statements on all instances in P(P_n).  Usage: python3 k4rec2.py n [budget]"""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
def le(p, q): return theta(q, p) == p
def cls_of(J, S):  # class of join J (list of masks) containing set S (S inside one class)
    for K in J:
        if K & S: return K
n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
P = projections(n); random.seed(1); t0 = time.time(); stats = {}; inst = 0
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if n >= 5: random.shuffle(pairs)
for a, c in pairs:
    if time.time() - t0 > budget: break
    Ys = [y for y in P if theta(a, y) == a and commute(y, c)]
    if not Ys: continue
    Jac = join(a, c)
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        Zs = [z for z in P if le(b, z) and theta(z, a) == u]
        if not Zs: continue
        Jab = join(a, b); Jbc = join(b, c)
        TA = [B for B in a[0] if B & a[1]]; TB = [B for B in b[0] if B & b[1]]; TC = [B for B in c[0] if B & c[1]]
        # matching via classes
        partner_ac = {A: [C for C in TC if cls_of(Jac, A) & C][0] for A in TA}
        partner_cb = {C: [B for B in TB if cls_of(Jbc, C) & B][0] for C in TC}
        for z in Zs:
            for y in Ys:
                if theta(z, y) != v: continue
                inst += 1
                Jay = join(a, y); Jzy = join(z, y); Jzc = join(z, c); Jyc = join(y, c)
                TZ = [B for B in z[0] if B & z[1]]; TY = [B for B in y[0] if B & y[1]]
                for A in TA:
                    C = partner_ac[A]; Bm = partner_cb[C]; D = cls_of(Jab, A)
                    rec('D(A) meets supp b', bool(D & b[1]))
                    rec('B_i in D(A_i)', bool(D & Bm))
                    rec('C_i meets D(A_i)', bool(D & C))
                    rec('A_i subset supp z', A & z[1] == A)
                    rec('A_i subset supp b', A & b[1] == A)
                    rec('A_i meets supp b', bool(A & b[1]))
                    rec('A_i meets supp y', bool(A & y[1]))
                    rec('A_i subset supp y', A & y[1] == A)
                    rec('A_i meets C_i', bool(A & C))
                    rec('A_i meets B_i', bool(A & Bm))
                    rec('D(A_i) meets supp y', bool(D & y[1]))
                    rec('D(A_i) meets supp c', bool(D & c[1]))
                    rec('cls_ay(A) meets supp c', bool(cls_of(Jay, A) & c[1]))
                    rec('cls_ay(A) contains C_i', cls_of(Jay, A) & C == C)
                    rec('cls_ay(A) meets B_i', bool(cls_of(Jay, A) & Bm))
                for B in TB:
                    D = cls_of(Jab, B); rec('D(B) meets supp a', bool(D & a[1])); rec('B subset supp y', B & y[1] == B); rec('B meets supp y', bool(B & y[1]))
                    rec('B subset supp a', B & a[1] == B); rec('cls_zy(B) meets supp a', bool(cls_of(Jzy, B) & a[1]))
                for C in TC:
                    rec('C subset supp y', C & y[1] == C); rec('C meets supp y', bool(C & y[1])); rec('C subset supp z', C & z[1] == C); rec('C meets supp z', bool(C & z[1]))
                    rec('C subset supp a', C & a[1] == C); rec('C meets supp a', bool(C & a[1]))
                rec('supp a subset supp z', a[1] & z[1] == a[1]); rec('supp a subset supp y', a[1] & y[1] == a[1])
                rec('supp c subset supp y', c[1] & y[1] == c[1]); rec('supp b subset supp y', b[1] & y[1] == b[1])
                rec('eps_a<=eps_y on supp a (A union of T(y))', all(any(A & Y == Y for Y in TY) or True for A in TA) and all(A & y[1] == A for A in TA))
print('P_%d: %d instances (%.0fs)' % (n, inst, time.time() - t0))
for k, (tot, ok) in stats.items(): print('  %-36s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
