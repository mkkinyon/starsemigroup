"""Reviewer's check of every intermediate claim of the proof of Theorem 5.49 (K4) on the K4-instances of P(P_4)
(code/k4inst4.pkl) and on random instances of P(P_5).  Usage: python3 k4verify.py [p5_seconds]
Each claim is recorded as name -> (instances tested, instances where it holds)."""
import sys, pickle, time, random, itertools
sys.path.insert(0, '/home/claude/pa8w/review3/code')
from fast import projections, theta, join, commute, matched, show

stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += bool(val)
def le(p, q): return theta(q, p) == p
def cls_of(J, S):
    for K in J:
        if K & S: return K
    raise ValueError
def blocks_T(p): return [B for B in p[0] if B & p[1]]
def blocks_N(p): return [B for B in p[0] if not (B & p[1])]
def block_of(p, x):
    for B in p[0]:
        if B >> x & 1: return B
def nclasses(J, Y=None):
    return len(J) if Y is None else sum(1 for K in J if K & Y)
def joinmasks(*ps):
    """join of the partitions of several projections (as list of class masks)."""
    cur = ps[0]
    for q in ps[1:]:
        cur = (tuple(join(cur, q)), 0)
    return list(cur[0])
def eq_part(J1, J2): return sorted(J1) == sorted(J2)
def pts(mask, n): return [x for x in range(n) if mask >> x & 1]

def check(I, n):
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    # hypotheses
    rec('H: a|><|c', matched(a, c)); rec('H: b|><|c', matched(b, c)); rec('H: theta_a(y)=a', theta(a, y) == a)
    rec('H: b<=z', le(b, z)); rec('H: yc=cy', commute(y, c))
    u = theta(a, b); v = theta(b, a)
    rec('H: theta_z(y)=v', theta(z, y) == v); rec('H: theta_z(a)=u', theta(z, a) == u)
    rec('CONCLUSION a|><|b', matched(a, b))
    m = len(blocks_T(a)); nn = len(blocks_T(u))
    # ---- Step 1 (algebra)
    rec('S1: theta_a(z)=theta_z(a)=u (az=za=u)', theta(a, z) == u and theta(z, a) == u)
    rec('S1: theta_b(y)=v', theta(b, y) == v)
    rec('S1: u|><|v', matched(u, v))
    rec('S1: theta_u(y)=u', theta(u, y) == u); rec('S1: theta_u(c)=u', theta(u, c) == u)
    rec('S1: theta_z(c)=b (Prover9 k4.pf1)', theta(z, c) == b)
    rec('S1: theta_y(u)=theta_y(z)', theta(y, u) == theta(y, z))
    rec('S1: theta_y(theta_b(x))=theta_y(theta_z(x)) all x', all(theta(y, theta(b, x)) == theta(y, theta(z, x)) for x in PROJ[n]))
    # ---- geometry
    TA, TB, TC, TY, TZ = blocks_T(a), blocks_T(b), blocks_T(c), blocks_T(y), blocks_T(z)
    Jac, Jbc, Jab, Jaz, Jay, Jzy, Jzc, Jyc, Jby = join(a, c), join(b, c), join(a, b), join(a, z), join(a, y), join(z, y), join(z, c), join(y, c), join(b, y)
    Omega = joinmasks(a, b, c); M = joinmasks(a, z, y)
    # matchings A_i -> C_i -> B_i
    Cof = {A: [C for C in TC if cls_of(Jac, A) & C][0] for A in TA}
    Bof = {C: [B for B in TB if cls_of(Jbc, C) & B][0] for C in TC}
    Gamma = {A: cls_of(Jac, A) for A in TA}; Delta = {C: cls_of(Jbc, C) for C in TC}
    # ---- Step 2
    rec('S2: eps_u = eps_a v eps_z', eq_part(list(u[0]), Jaz))
    rec('S2: T(u)-blocks = type (i) classes of (a,z)', sorted(blocks_T(u)) == sorted(K for K in Jaz if K & a[1] and K & z[1]))
    rec('S2: eps_z <= eps_b, supp b <= supp z', all(any(Z & B == Z for B in b[0]) for Z in z[0]) and b[1] & ~z[1] == 0)
    rec('S2: eps_u v eps_v = eps_a v eps_b', eq_part(join(u, v), Jab))
    rec('S2 CLAIM: supp a <= supp z (no type (ii))', a[1] & ~z[1] == 0)
    Ks = blocks_T(u)
    Ds = {K: cls_of(Jab, K) for K in Ks}
    Ss = {K: Ds[K] & b[1] for K in Ks}
    rec('S2: S_j = D_j cap supp b is a T(v)-block', all(S in blocks_T(v) for S in Ss.values()) and len(set(Ss.values())) == nn and sorted(Ss.values()) == sorted(blocks_T(v)))
    # the delta' identity for (b,c), v<=b, and the claim "left side is n"
    lhs = nclasses(list(v[0]), b[1]); rhs = nclasses(join(v, c), c[1])
    rec("S2: |eps_v|_{supp b} = |eps_v v eps_c|_{supp c}", lhs == rhs)
    rec("S2: 'left side is n'  (|eps_v|_{supp b} == rk u)", lhs == nn)
    rec('S2 CLAIM: every B_i lies in some S_j (supp v = supp b)', v[1] == b[1])
    rec('S2: N(v)-blocks inside supp b: none', not any(B & b[1] for B in blocks_N(v)))
    # delta' identity for (a,c), u<=a
    lhs2 = nclasses(list(u[0]), a[1]); rhs2 = nclasses(Omega, c[1])
    rec("S2: |eps_u|_{supp a} = |Omega|_{supp c}", lhs2 == rhs2); rec("S2: |Omega|_{supp c} = n", rhs2 == nn)
    rec('S2: each Omega-class meeting supp u contains exactly one K_j', all(sum(1 for K in Ks if K & O) == 1 for O in Omega if O & u[1]))
    NZ = blocks_N(z)
    rec('S2: supp u = supp a', u[1] == a[1])
    rec('S2: N(z)-blocks = common N-blocks of a,b,z (outer)', all(O in blocks_N(a) and O in blocks_N(b) for O in NZ))
    rec('S2: N(a)-block inside supp z is union of T(z)', all(all((Z & P == 0) or (Z & P == Z) for Z in TZ) for P in blocks_N(a) if P & z[1]))
    rec('S2: every class of eps_a v eps_b meeting supp a or supp b is some D_j', all(D in Ds.values() for D in Jab if D & (a[1] | b[1])))
    rec('S2: D_j <= supp z', all(D & ~z[1] == 0 for D in Ds.values()))
    rec('S2: A_i<=K_j iff B_i<=S_j', all(((A & K) == A) == ((Bof[Cof[A]] & Ss[K]) == Bof[Cof[A]]) for A in TA for K in Ks))
    # ---- Step 3
    rec('S3: eps_b <= eps_z v eps_c', all(any(B & K == B for K in Jzc) for B in b[0]))
    rec('S3: eps_z v eps_c = eps_b v eps_c', eq_part(Jzc, Jbc))
    rec('S3: Delta_i cap supp z = B_i', all(Delta[C] & z[1] == Bof[C] for C in TC))
    rec('S3: every c-block meets supp z inside a single b-block', all(len({block_of(b, x) for x in pts(E & z[1], n)}) <= 1 for E in c[0]))
    # classes K' of eps_z v eps_y meeting supp z
    ok1 = ok2 = True
    for K in Jzy:
        if not (K & z[1]): continue
        inter = K & z[1]
        if inter in Ss.values():
            ok1 = ok1 and bool(K & y[1])
        elif inter in blocks_N(b):
            ok2 = ok2 and not (K & y[1])
        else:
            ok1 = False
    rec("S3: K' cap supp z = some S_j (meets supp y) or an N(b)-block (does not)", ok1 and ok2)
    rec('S3: eps_b <= eps_z v eps_y', all(any(B & K == B for K in Jzy) for B in b[0]))
    rec('S3: eps_z v eps_y = eps_b v eps_y', eq_part(Jzy, Jby))
    NC = blocks_N(c); Cun = sum(TC)
    rec('S3: y-block meeting N(c)-block lies inside it', all((Y & E == 0) or (Y & E == Y) for Y in y[0] for E in NC))
    rec('S3: y-block meeting no N(c)-block is inside union C_i', all(Y & ~Cun == 0 for Y in y[0] if not any(Y & E for E in NC)))
    # ---- Step 4
    Es = {A: cls_of(Jay, A) for A in TA}
    rec('S4: classes of eps_a v eps_y meeting supp a: E_i cap supp a = A_i, meets supp y', all(E & a[1] == A and E & y[1] for A, E in Es.items()) and all(any(K & A for A in TA) for K in Jay if K & a[1]))
    Ms = {K: cls_of(M, K) for K in Ks}
    rec('S4: classes of M meeting supp a: M_j cap supp a = K_j', all(Mj & a[1] == K for K, Mj in Ms.items()) and all(any(K & Kj for Kj in Ks) for K in M if K & a[1]))
    rec('S4: |eps_u|-|Omega| = |eps_a|-|eps_a v eps_c|', len(u[0]) - len(Omega) == len(a[0]) - len(Jac))
    rec('S4: |M|-|Omega| = |eps_a v eps_y|-|eps_a v eps_c|', len(M) - len(Omega) == len(Jay) - len(Jac))
    rec('S4: |eps_a v eps_y|-|M| = m-n', len(Jay) - len(M) == m - nn)
    rec('S4: M_j = union of E_i, i in I_j', all(Mj == sum(set(Es[A] for A in TA if A & K)) for K, Mj in Ms.items()))
    Kp = {K: cls_of(Jzy, Ss[K]) for K in Ks}
    rec("S4: D_j <= M_j, K'_j <= M_j", all(Ds[K] & ~Ms[K] == 0 and Kp[K] & ~Ms[K] == 0 for K in Ks))
    rec("S4: T-blocks of theta_y(u) and theta_y(z) are the M_j cap supp y = K'_j cap supp y", all(Ms[K] & y[1] == Kp[K] & y[1] for K in Ks))
    rec("S4: every T(y)-block inside M_j lies in K'_j", all(all((Y & Ms[K] == 0) or (Y & Kp[K] == Y) for Y in TY) for K in Ks))
    rec("S4: K'_j cap supp z = S_j", all(Kp[K] & z[1] == Ss[K] for K in Ks))
    # ---- Step 5: labels (checked for every K'_j, also when |I_j| = 1)
    idx = {A: i for i, A in enumerate(TA)}
    Ci = {Cof[A]: idx[A] for A in TA}; Bi = {Bof[Cof[A]]: idx[A] for A in TA}
    def gamma(x):
        G = cls_of(Jac, block_of(c, x)); As = [A for A in TA if A & G]
        return idx[As[0]] if As else None
    def lam(x):
        D = cls_of(Jbc, block_of(c, x)); Bs = [B for B in TB if B & D]
        return Bi[Bs[0]] if Bs else None
    outer = set(NZ)
    for K in Ks:
        Ij = [idx[A] for A in TA if A & K]
        Kj = Kp[K]
        def sigma(x):
            P = block_of(a, x); E = cls_of(Jay, P); As = [A for A in TA if A & E]
            assert len(As) == 1 and idx[As[0]] in Ij; return idx[As[0]]
        labels = {x: (sigma(x), gamma(x), lam(x)) for x in pts(Kj, n)}
        rec("S5: sigma well defined on K'_j (a-block inside some E_i, i in I_j)", True)
        # block-wise label changes
        for Z in z[0]:
            if not (Z & Kj): continue
            L = {labels[x] for x in pts(Z, n)}
            if Z in outer: rec('S5: labels constant on outer block', len(L) == 1)
            else:
                rec('S5: T(z)-block in K\'_j lies in S_j', Z & Ss[K] == Z)
                rec('S5: T(z)-block: lambda constant', len({l[2] for l in L}) == 1)
                rec('S5: T(z)-block: labels (i,i,k) or constant', len(L) == 1 or all(l[0] == l[1] for l in L))
        for Y in y[0]:
            if not (Y & Kj): continue
            L = {labels[x] for x in pts(Y, n)}
            rec('S5: y-block: sigma constant', len({l[0] for l in L}) == 1)
            rec('S5: y-block: labels (s,i,i) or constant', len(L) == 1 or all(l[1] == l[2] for l in L))
        # component: with |I_j|=1 (always in P_4/P_5) the labels should lie in C_s with s = the unique i
        Lset = set(labels.values())
        comp_ok = {s for s in Ij if all((l[0] == s and l[1] == l[2] and l[1] is not None) or (l[0] == l[1] and l[2] == s) for l in Lset)}
        rec("S5: labels of K'_j lie in a single component C_s", len(comp_ok) >= 1)
        rec("S5: no point of K'_j has gamma or lambda = empty", all(l[1] is not None and l[2] is not None for l in Lset))
        if len(Ij) == 1:
            rec("S5 (|I_j|=1): every point of K'_j has gamma = lambda", all(l[1] == l[2] for l in Lset))
    rec('|I_j| = 1 for all j', all(sum(1 for A in TA if A & K) == 1 for K in Ks))

PROJ = {}
if __name__ == '__main__':
    PROJ[4] = projections(4)
    INST = pickle.load(open('/home/claude/pa8w/review3/code/k4inst4.pkl', 'rb'))
    t0 = time.time()
    for I in INST: check(I, 4)
    print('P_4: %d instances (%.0fs)' % (len(INST), time.time() - t0))
    for k, (tot, ok) in stats.items(): print('  %-75s %7d/%-7d %s' % (k, ok, tot, 'ALWAYS' if ok == tot else ('NEVER' if ok == 0 else 'SOMETIMES')))
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 0
    if budget > 0:
        stats.clear(); P = projections(5); PROJ[5] = P; random.seed(2026); t0 = time.time(); cnt = 0
        pairs = [(a, c) for a in P for c in P if matched(a, c)]; random.shuffle(pairs)
        for a, c in pairs:
            if time.time() - t0 > budget: break
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
        print('P_5: %d random instances (%.0fs)' % (cnt, time.time() - t0))
        for k, (tot, ok) in stats.items(): print('  %-75s %7d/%-7d %s' % (k, ok, tot, 'ALWAYS' if ok == tot else ('NEVER' if ok == 0 else 'SOMETIMES')))
