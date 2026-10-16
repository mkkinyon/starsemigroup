"""Referee's independent check of the intermediate claims of the K0 proof (thmK0.tex), 16 Oct.
Projection = (tuple of block bitmasks, T bitmask) as in review2/review-scripts/fast.py (reviewer's calculus).
Usage: python3 k0claims_ref.py 4            (all instances of k0inst4.pkl)
       python3 k0claims_ref.py 5 200000     (random sample of k0inst5.pkl)
"""
import sys, pickle, random, time
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import theta, join, commute, matched

def blocks(p): return p[0]
def T(p): return [b for b in p[0] if b & p[1]]
def N(p): return [b for b in p[0] if not (b & p[1])]
def rk(p): return len(T(p))
def cls_of(classes, x):           # class (bitmask) containing bitmask x (x must lie inside one class)
    for K in classes:
        if K & x: return K
    raise ValueError
def in_one(classes, S):            # S lies in a single class
    return any((S & K) == S for K in classes)
def leq(p, q):                     # p <= q  iff theta_q(p) = p
    return theta(q, p) == p

def check(inst):
    a, b, c, y, z = inst['a'], inst['b'], inst['c'], inst['y'], inst['z']
    R = {}
    sa, sb, sc, sy, sz = a[1], b[1], c[1], y[1], z[1]
    Na, Nb, Nc, Ny, Nz = set(N(a)), set(N(b)), set(N(c)), set(N(y)), set(N(z))
    Ta, Tb, Tc, Ty = T(a), T(b), T(c), T(y)
    m = len(Ta)
    # ---- hypotheses (sanity) ----
    R['hyp'] = (matched(a, c) and matched(c, b) and commute(y, c) and theta(y, b) == theta(b, a)
                and theta(b, z) == b and theta(z, a) == theta(z, b) and theta(y, z) == theta(a, b))
    # ---- Theorem thm:R indexing: Gamma_i, C_i, Delta_i, B_i ----
    Gac = join(a, c); Gbc = join(b, c)
    A = Ta
    Gam = [cls_of(Gac, Ai) for Ai in A]
    C = []
    for G in Gam:
        cs = [Ci for Ci in Tc if Ci & G]
        assert len(cs) == 1; C.append(cs[0])
    Del = [cls_of(Gbc, Ci) for Ci in C]
    B = []
    for D in Del:
        bs = [Bi for Bi in Tb if Bi & D]
        assert len(bs) == 1; B.append(bs[0])
    assert len(set(B)) == m == len(set(C))
    u = theta(a, b); v = theta(b, a); n = rk(u)
    # ---- Step 1 ----
    R['u<=a,v<=b,u<=y,v<=y'] = leq(u, a) and leq(v, b) and leq(u, y) and leq(v, y)
    R['ya=ay, by=yb'] = commute(y, a) and commute(y, b)
    R['theta_y(a)=u'] = theta(y, a) == u
    R['theta_y(b)=v'] = theta(y, b) == v
    p = theta(z, a)
    R['rk p = m'] = rk(p) == m
    R['theta_a(z)=a'] = theta(a, z) == a
    Gaz = join(a, z); Gbz = join(b, z)
    L = [cls_of(Gaz, Ai) for Ai in A]; Lp = [cls_of(Gbz, Bi) for Bi in B]
    R['L_i distinct, Lp_i distinct'] = len(set(L)) == m and len(set(Lp)) == m
    cells = [K & Kp for K in Gaz for Kp in Gbz if K & Kp]
    D = [L[i] & Lp[i] for i in range(m)]
    Dun = 0
    for d in D: Dun |= d
    R['some diagonal cell empty (info)'] = any(d == 0 for d in D)
    # ---- Step 2 ----
    Gya = join(y, a); Gyb = join(y, b); Gyc = join(y, c)
    R['every A_i meets supp y'] = all(Ai & sy for Ai in A)
    R['every B_i meets supp y'] = all(Bi & sy for Bi in B)
    def union_of(S, blks):  # S is a (nonempty) union of blocks from blks
        return S and all(((bl & S) == 0) or ((bl & S) == bl) for bl in blks) and S & sum(blks) == S
    R['no N(y)-block is a union of T(a)-blocks'] = not any(union_of(Nn, Ta) for Nn in Ny)
    R['no N(y)-block is a union of T(b)-blocks'] = not any(union_of(Nn, Tb) for Nn in Ny)
    R['N(y)-blocks are N(a)-blocks'] = Ny <= Na
    R['N(y)-blocks are N(b)-blocks'] = Ny <= Nb
    R['N(y)-blocks are N(c)-blocks (not claimed)'] = Ny <= Nc
    def Tblock_conf(Y, Tq, Nq):   # Y lies in a union of T(q)-blocks or inside an N(q)-block
        return (Y & sum(Tq)) == Y or any((Y & F) == Y for F in Nq)
    R['T(y)-block in supp a or in an N(a)-block'] = all(Tblock_conf(Y, Ta, Na) for Y in Ty)
    R['T(y)-block in supp b or in an N(b)-block'] = all(Tblock_conf(Y, Tb, Nb) for Y in Ty)
    R['T(y)-block in supp c or in an N(c)-block'] = all(Tblock_conf(Y, Tc, Nc) for Y in Ty)
    R['N-block of a,b,c meeting a T(y)-block contains it'] = all(
        (Y & F) == 0 or (Y & F) == Y for Y in Ty for F in Na | Nb | Nc)
    # type (i) classes of eps_y v eps_a
    U = [K for K in Gya if (K & sy) == K and (K & sa) == K]
    Mcl = [M for M in join(a, b) if M & sa]
    R['U_j = M_j & supp a (as sets)'] = sorted(U) == sorted(M & sa for M in Mcl)
    R['every M_j meets supp b'] = all(M & sb for M in Mcl)
    R['#U = n'] = len(U) == n
    R['rk(ya) = n'] = rk(theta(y, a)) == n
    R['u <= ya'] = leq(u, theta(y, a))
    Uof = {}
    for Ai in A:
        Uj = [Uk for Uk in U if Uk & Ai]
        R.setdefault('each A_i in exactly one U_j', True)
        if len(Uj) != 1 or (Ai & Uj[0]) != Ai: R['each A_i in exactly one U_j'] = False
        Uof[Ai] = Uj[0] if Uj else None
    # ---- Step 3 ----
    Gyz = join(y, z)
    Ks = [K for K in Gyz if K & sy]
    NaF = [F for F in Na if (F & sy) == F]
    ok3 = True
    for K in Ks:
        S = K & sy
        if S in U: ok3 = ok3 and bool(K & sz)
        elif S in NaF: ok3 = ok3 and not (K & sz)
        else: ok3 = False
    R['classes of y v z meeting supp y: K_j (meets supp z) / K_F (misses supp z)'] = ok3 and \
        sorted(K & sy for K in Ks) == sorted(U + NaF)
    R['K_F & supp a = 0 (Step 5 wording)'] = all((K & sa) == 0 for K in Ks if (K & sy) in NaF)
    # ---- Step 4 ----
    crossing = [Y for Y in Ty if sum(1 for Ai in A if Ai & Y) >= 2]
    noncross = [Y for Y in Ty if Y not in crossing]
    ok4a = True; ok4a2 = True
    for Y in crossing:
        S = 0
        for i in range(m):
            if Y & A[i]: S |= A[i] & B[i] & C[i]
        if (Y & S) != Y: ok4a = False
        if (Y & Dun) != Y: ok4a2 = False
    R['crossing Y in U(A_i&B_i&C_i), i with Y&A_i!=0'] = ok4a
    R['crossing Y in U D_i'] = ok4a2
    R['crossing Y meets an N(b)-block (info)'] = any(Y & F for Y in crossing for F in Nb)
    R['instance has a crossing block (info)'] = bool(crossing)
    R['some T(y)-block meets a point outside supp a|supp b|supp c (info)'] = any(Y & ~(sa | sb | sc) for Y in Ty)
    R['non-crossing T(y)-block in one cell'] = all(in_one(cells, Y) for Y in noncross)
    R['N(y)-block in one cell'] = all(in_one(cells, Nn) for Nn in Ny)
    R['z-block in one cell'] = all(in_one(cells, Z) for Z in blocks(z))
    ok4d = True
    for K in Gyz:
        if any(Y & K for Y in crossing):
            if (K & Dun) != K: ok4d = False
        elif not in_one(cells, K): ok4d = False
    R['class of y v z: one cell if no crossing block, else in U D_i'] = ok4d
    # ---- Step 5 ----
    ok5 = True; ok5b = True
    for i in range(m):
        K = cls_of(Gyz, A[i])
        if any(Y & K for Y in crossing):
            if (A[i] & D[i]) != A[i]: ok5 = False
        else:
            if not in_one(cells, A[i]): ok5 = False
        if (A[i] & Lp[i]) != A[i]: ok5b = False
    R['A_i in D_i if K_j has a crossing block, else in one cell'] = ok5
    R['A_i in Lp_i always (not claimed)'] = ok5b
    R['eps_a <= eps_b v eps_z'] = all(in_one(Gbz, bl) for bl in blocks(a))
    R['eps_a v eps_b <= eps_b v eps_z'] = all(in_one(Gbz, M) for M in join(a, b))
    # ---- Step 6 ----
    R['U_j with >=2 A_i contains a crossing block'] = all(
        any((Y & Uk) == Y for Y in crossing) for Uk in U if sum(1 for Ai in A if Ai & Uk) >= 2)
    R['n = m'] = n == m
    R['a><b'] = matched(a, b)
    R['m = 1 (info)'] = m == 1
    R['m = 0 (info)'] = m == 0
    R['a = b (info)'] = a == b
    return R

if __name__ == '__main__':
    nn = int(sys.argv[1]); sample = int(sys.argv[2]) if len(sys.argv) > 2 else None
    I = pickle.load(open('/home/claude/pa8w/embed/pa8/k0/k0inst%d.pkl' % nn, 'rb'))
    if sample:
        random.seed(20261016); I = random.sample(I, sample)
    t0 = time.time(); fails = {}; cnt = 0; ms = {}; ncross = 0
    for inst in I:
        R = check(inst); cnt += 1
        m = rk(inst['a']); ms[m] = ms.get(m, 0) + 1
        for k, vv in R.items():
            fails.setdefault(k, 0)
            if '(info)' in k:
                if vv: fails[k] += 1
            elif not vv: fails[k] += 1
    print('P_%d: %d instances checked (%.0fs); rows = FAILS/instances; "(info)" rows = instances where the property holds' % (nn, cnt, time.time() - t0))
    print('distribution of m = rk a:', sorted(ms.items()))
    for k, vv in fails.items():
        print('%-75s %8d / %d' % (k, vv, cnt))
