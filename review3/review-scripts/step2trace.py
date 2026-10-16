"""Walk through the sentences of Step 2 of Thm 5.49 on instances of P(P_4) satisfying every K4 hypothesis except
aya = a (so that all inputs actually used by Step 2 hold: a|><|c, b|><|c, b<=z, theta_z(a)=u, theta_z(y)=v, yc=cy,
and the Prover9 lemma theta_z(c)=b), and report which sentence is the first false one."""
import sys
sys.path.insert(0, '/home/claude/pa8w/review3/code')
from fast import projections, theta, join, commute, matched, show
n = 4; P = projections(n)
le = lambda p, q: theta(q, p) == p
def cls_of(J, S):
    for K in J:
        if K & S: return K
def bT(p): return [B for B in p[0] if B & p[1]]
def bN(p): return [B for B in p[0] if not (B & p[1])]
def ncl(J, Y): return sum(1 for K in J if K & Y)
def jm(*ps):
    cur = ps[0]
    for q in ps[1:]: cur = (tuple(join(cur, q)), 0)
    return list(cur[0])
found = 0; first = {}
for a in P:
    for c in P:
        if not matched(a, c): continue
        for b in P:
            if not matched(b, c): continue
            u = theta(a, b); v = theta(b, a)
            for z in P:
                if not (le(b, z) and theta(z, a) == u): continue
                for y in P:
                    if theta(a, y) == a or not commute(y, c) or theta(z, y) != v: continue
                    assert theta(z, c) == b and matched(u, v) and theta(u, c) == u
                    nn = len(bT(u))
                    # sentence A: "the left side is n"
                    lhs = ncl(list(v[0]), b[1]); rhs = ncl(join(v, c), c[1])
                    # sentence B: every B_i lies in some S_j
                    claimB = v[1] == b[1]
                    # sentence C: right side |Omega|_{supp c} = n
                    Om = jm(a, b, c); rhs2 = ncl(Om, c[1]); lhs2 = ncl(list(u[0]), a[1])
                    key = ('lhs==rhs', lhs == rhs, 'lhs==n', lhs == nn, 'claimB', claimB, '|Omega|_c==n', rhs2 == nn, '|eps_u|_a==|Omega|_c', lhs2 == rhs2, 'supp a<=supp z', a[1] & ~z[1] == 0)
                    first.setdefault(key, (a, b, c, y, z, lhs, rhs, nn, lhs2, rhs2)); found += 1
print('instances with all K4 hypotheses except aya=a:', found)
for key, (a, b, c, y, z, lhs, rhs, nn, lhs2, rhs2) in first.items():
    cnt = 0
    print(key)
    print('   e.g. a=%s b=%s c=%s y=%s z=%s;  u=%s v=%s;  |eps_v|_{supp b}=%d |eps_v v eps_c|_{supp c}=%d n=%d; |eps_u|_{supp a}=%d |Omega|_{supp c}=%d'
          % (show(a, n), show(b, n), show(c, n), show(y, n), show(z, n), show(theta(a, b), n), show(theta(b, a), n), lhs, rhs, nn, lhs2, rhs2))
