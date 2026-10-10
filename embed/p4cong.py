"""The mu-type *-congruences of P_n (n = 3, 4): mu = Delta u {(a,b) in I_1 x I_1 : hat(a) = hat(b)},
where hat cuts the transversal block of a rank-<=1 partition; variant mu2 = mu plus the pairs of
rank-2 elements in the same H-class (mod S_2).  Verify the congruence property against generators,
then test Q1 and the triangle condition on the projection algebra of the quotient.
Usage: python3 p4cong.py n"""
import sys, time, itertools
from collections import defaultdict
from pmon import partition_monoid, mul, star, rank, canon, is_projection
from digraph import clause, parse_clause, search

n = int(sys.argv[1])
elems = partition_monoid(n); idx = {e: i for i, e in enumerate(elems)}
N = len(elems); print(f"P_{n}: {N} elements", flush=True)
rk = [rank(e, n) for e in elems]

def hat(p):
    out = []
    for b in p:
        up = [x for x in b if x < n]; lo = [x for x in b if x >= n]
        if up and lo: out += [tuple(up), tuple(lo)]
        else: out.append(tuple(b))
    return tuple(sorted(out))

def classes_mu(variant):
    cls = list(range(N))            # class representative id
    key = {}
    for i, e in enumerate(elems):
        if rk[i] <= 1:
            k = ("hat", hat(e))
        elif variant == 2 and rk[i] == 2:
            # H-class: (upper partition with transversal marks, lower partition with marks)
            up = tuple(sorted(tuple(x for x in b if x < n) for b in e if any(x < n for x in b)))
            lo = tuple(sorted(tuple(x for x in b if x >= n) for b in e if any(x >= n for x in b)))
            tu = tuple(sorted(tuple(x for x in b if x < n) for b in e if any(x < n for x in b) and any(x >= n for x in b)))
            tl = tuple(sorted(tuple(x for x in b if x >= n) for b in e if any(x < n for x in b) and any(x >= n for x in b)))
            k = ("H", up, lo, tu, tl)
        else:
            k = ("id", i)
        key.setdefault(k, i); cls[i] = key[k]
    return cls

def generators():
    gens = []
    # transposition (0 1), n-cycle, merge {0,1}, cut point 0
    perm = list(range(n)); perm[0], perm[1] = 1, 0
    gens.append(canon([[i, n + perm[i]] for i in range(n)]))
    cyc = [(i + 1) % n for i in range(n)]
    gens.append(canon([[i, n + cyc[i]] for i in range(n)]))
    gens.append(canon([[0, 1, n, n + 1]] + [[i, n + i] for i in range(2, n)]))
    gens.append(canon([[0], [n]] + [[i, n + i] for i in range(1, n)]))
    return gens

def is_congruence(cls):
    gens = generators()
    # star-compatibility
    for i, e in enumerate(elems):
        if cls[idx[star(e, n)]] != cls[idx[star(elems[cls[i]], n)]]: return False, "star"
    groups = defaultdict(list)
    for i in range(N): groups[cls[i]].append(i)
    for members in groups.values():
        if len(members) == 1: continue
        r = members[0]
        for g in gens:
            for side in (0, 1):
                ref = cls[idx[mul(g, elems[r], n) if side == 0 else mul(elems[r], g, n)]]
                for m in members[1:]:
                    v = cls[idx[mul(g, elems[m], n) if side == 0 else mul(elems[m], g, n)]]
                    if v != ref: return False, (g, side, r, m)
    return True, None

for variant in (1, 2):
    cls = classes_mu(variant)
    ncl = len(set(cls))
    ok, why = is_congruence(cls)
    print(f"variant {variant}: {ncl} classes; congruence: {ok} {why if not ok else ''}", flush=True)
    if not ok: continue
    # projection algebra of the quotient: classes of projections
    projs = sorted({cls[i] for i, e in enumerate(elems) if is_projection(e, n)})
    pidx = {c: k for k, c in enumerate(projs)}
    def theta(x, y):     # x * y = y x y in the quotient, on class reps
        ex, ey = elems[x], elems[y]
        return cls[idx[mul(mul(ey, ex, n), ey, n)]]
    T = [[pidx[theta(projs[a], projs[b])] for b in range(len(projs))] for a in range(len(projs))]
    K = len(projs); print(f"   {K} projections in the quotient", flush=True)
    # sanity: every theta of projections is a projection class
    # Q1: r*p = r & r*q = r -> p*q = q*p
    q1 = all(T[p][q] == T[q][p] for p in range(K) for q in range(K)
             if any(T[r][p] == r and T[r][q] == r for r in range(K)))
    print(f"   Q1: {q1}", flush=True)
    op = lambda x, y: T[x][y]
    t = time.time()
    tri = search(parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)])), range(K), op, limit=3000)
    print(f"   triangle condition: {'holds' if tri == [] else ('timeout' if tri == 'timeout' else 'FAILS')} ({time.time()-t:.0f}s)", flush=True)
    if tri and tri != "timeout":
        env = tri[0]
        for v in sorted(env): print("     ", v, elems[projs[env[v]]])
