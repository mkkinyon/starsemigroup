"""Which intermediate statements of the proof of Thm 5.49 survive when one K4 hypothesis is dropped (P_4)?
A statement that fails when hypothesis h is dropped cannot be proved without h.  Usage: python3 dropmap.py [n]"""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review3/code')
from fast import projections, theta, join, commute, matched, show
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
P = projections(n); t0 = time.time()
le = lambda p, q: theta(q, p) == p
def cls_of(J, S):
    for K in J:
        if K & S: return K
def bT(p): return [B for B in p[0] if B & p[1]]
def bN(p): return [B for B in p[0] if not (B & p[1])]
def blk(p, x):
    for B in p[0]:
        if B >> x & 1: return B
def jm(*ps):
    cur = ps[0]
    for q in ps[1:]: cur = (tuple(join(cur, q)), 0)
    return list(cur[0])

def statements(a, b, c, y, z):
    u = theta(a, b); v = theta(b, a); S = {}
    TA, TB, TC = bT(a), bT(b), bT(c)
    Jac, Jbc, Jab, Jaz, Jay, Jzy = join(a, c), join(b, c), join(a, b), join(a, z), join(a, y), join(z, y)
    Cof = {A: [C for C in TC if cls_of(Jac, A) & C][0] for A in TA}
    Bof = {C: [B for B in TB if cls_of(Jbc, C) & B][0] for C in TC}
    S['a|><|b'] = matched(a, b)
    S['supp a <= supp z'] = a[1] & ~z[1] == 0
    S['supp v = supp b (every B_i in some S_j)'] = v[1] == b[1]
    S['supp u = supp a'] = u[1] == a[1]
    S['theta_z(c) = b'] = theta(z, c) == b
    S['theta_y(u) = theta_y(z)'] = theta(y, u) == theta(y, z)
    S['eps_z v eps_c = eps_b v eps_c'] = sorted(join(z, c)) == sorted(Jbc)
    S['Delta_i cap supp z = B_i'] = all(cls_of(Jbc, C) & z[1] == Bof[C] for C in TC)
    S['eps_z v eps_y = eps_b v eps_y'] = sorted(Jzy) == sorted(join(b, y))
    S['N(z)-blocks are a-blocks and b-blocks'] = all(O in a[0] and O in b[0] for O in bN(z))
    Ks = bT(u)
    S['each Omega-class meeting supp c contains a K_j'] = all(any(K & O for K in Ks) for O in jm(a, b, c) if O & c[1])
    S['every c-block meeting B_i lies in Gamma_i'] = all(all(cls_of(Jac, blk(c, x)) & A for x in range(n) if Bof[Cof[A]] >> x & 1) for A in TA)
    S['B_i inside E_i (class of eps_a v eps_y of A_i)'] = all(cls_of(Jay, A) & Bof[Cof[A]] == Bof[Cof[A]] for A in TA)
    S['no y-block meets two T(b)-blocks'] = all(sum(1 for B in TB if B & Y) <= 1 for Y in y[0])
    S['no T(z)-block meets two T(a)-blocks'] = all(sum(1 for A in TA if A & Z) <= 1 for Z in bT(z))
    S['eps_z <= eps_a v eps_c'] = all(any(Z & K == Z for K in Jac) for Z in z[0])
    S['class of eps_z v eps_y of B_i meets supp y'] = all(cls_of(Jzy, B) & y[1] for B in TB)
    S['K_j: |I_j| = 1'] = all(sum(1 for A in TA if A & K) == 1 for K in Ks)
    S['u <= z, v <= z, u|><|v'] = le(u, z) and le(v, z) and matched(u, v)
    return S

res = {}
def bump(k, inst):
    S = statements(*inst)
    d = res.setdefault(k, {})
    for name, val in S.items():
        s = d.setdefault(name, [0, 0, None]); s[0] += 1; s[1] += bool(val)
        if not val and s[2] is None: s[2] = inst
pairs = [(a, c) for a in P for c in P if matched(a, c)]
for a, c in pairs:
    Y3 = [y for y in P if theta(a, y) == a]
    Y5 = [y for y in P if commute(y, c)]
    Y = [y for y in Y3 if commute(y, c)]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a)
        Z4 = [z for z in P if theta(z, a) == u]
        Z7 = [z for z in P if le(b, z)]
        Z = [z for z in Z4 if le(b, z)]
        for z in Z:
            for y in Y:
                if theta(z, y) == v: bump('full', (a, b, c, y, z))
                else: bump('drop theta_z(y)=v', (a, b, c, y, z))
            for y in Y3:
                if theta(z, y) == v and not commute(y, c): bump('drop yc=cy', (a, b, c, y, z))
            for y in Y5:
                if theta(z, y) == v and theta(a, y) != a: bump('drop theta_a(y)=a', (a, b, c, y, z))
        for z in Z4:
            if le(b, z): continue
            for y in Y:
                if theta(z, y) == v: bump('drop b<=z', (a, b, c, y, z))
        for z in Z7:
            if theta(z, a) == u: continue
            for y in Y:
                if theta(z, y) == v: bump('drop theta_z(a)=u', (a, b, c, y, z))
print('P_%d (%.0fs).  Entries: number of instances (hypotheses minus one) where the statement FAILS / total' % (n, time.time() - t0))
keys = sorted(res); names = list(res['full'])
print('%-52s' % 'statement' + ''.join('%18s' % k.replace('drop ', '-') for k in keys))
for name in names:
    print('%-52s' % name + ''.join('%18s' % ('%d/%d' % (res[k][name][0] - res[k][name][1], res[k][name][0])) for k in keys))
print()
for k in keys:
    for name in names:
        s = res[k][name]
        if s[2] is not None and name in ('supp a <= supp z', 'supp v = supp b (every B_i in some S_j)', 'every c-block meeting B_i lies in Gamma_i', 'theta_z(c) = b'):
            print('  [%s] %s fails e.g. at a=%s b=%s c=%s y=%s z=%s' % (k, name, *[show(p, n) for p in s[2]]))
