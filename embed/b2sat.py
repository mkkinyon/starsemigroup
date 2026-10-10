"""SAT: configurations for (S)'s hypotheses in P_m with z = cdc having no T-blocks (Case B), supp a
disjoint from supp b (Case B2), and rank a >= 2. Elements: 0=a,1=b,2=c,3=d,4=z,5=w."""
import sys, itertools, time
from pysat.solvers import Cadical153
from pysat.formula import IDPool
import pa_sat
def run(m, b2=True, rank2=True):
    # projection algebra partial table: we only need hypotheses, not a full table. Build clauses by hand:
    # reuse pa_sat machinery by giving a table with the needed products only? pa_sat needs a full table.
    # Instead: full table of the 6-element algebra is unknown (not M172). Encode directly.
    k = 8; pool = IDPool(); cls = []; X = range(m)
    def E(p, x, y):
        if x > y: x, y = y, x
        return pool.id(("e", p, x, y))
    def Tl(p, x): return pool.id(("t", p, x))
    def J(p, q, x, y):
        if p > q: p, q = q, p
        if x > y: x, y = y, x
        return pool.id(("J", p, q, x, y))
    for p in range(k):
        for x, y, z in itertools.permutations(X, 3):
            if x < z: cls.append([-E(p, x, y), -E(p, y, z), E(p, x, z)])
        for x in X:
            for y in X:
                if x < y:
                    cls.append([-E(p, x, y), -Tl(p, x), Tl(p, y)]); cls.append([-E(p, x, y), Tl(p, x), -Tl(p, y)])
    L = max(1, (m - 1).bit_length())
    def join(p, q):
        def R(i, x, y):
            if x > y: x, y = y, x
            return pool.id(("R", p, q, i, x, y))
        for x in X:
            for y in X:
                if x < y:
                    r0 = R(0, x, y); cls.append([-r0, E(p, x, y), E(q, x, y)]); cls.append([r0, -E(p, x, y)]); cls.append([r0, -E(q, x, y)])
        for i in range(L):
            for x in X:
                for y in X:
                    if x < y:
                        aux = []
                        for u in X:
                            if u in (x, y): continue
                            a = pool.id(("aux", p, q, i, x, y, u)); cls.append([-a, R(i, x, u)]); cls.append([-a, R(i, u, y)]); cls.append([a, -R(i, x, u), -R(i, u, y)]); aux.append(a)
                        nxt = R(i + 1, x, y); cls.append([-nxt, R(i, x, y)] + aux); cls.append([nxt, -R(i, x, y)])
                        for a in aux: cls.append([nxt, -a])
        for x in X:
            for y in X:
                if x < y: cls.append([-J(p, q, x, y), R(L, x, y)]); cls.append([J(p, q, x, y), -R(L, x, y)])
    def product(p, q, r):   # r = p q p
        for x in X:
            cls.append([Tl(p, x), -Tl(r, x)])
            ws = []
            for y in X:
                w = pool.id(("w", p, q, x, y))
                if y == x: cls.append([-w, Tl(q, y)]); cls.append([w, -Tl(q, y)])
                else: cls.append([-w, J(p, q, x, y)]); cls.append([-w, Tl(q, y)]); cls.append([w, -J(p, q, x, y), -Tl(q, y)])
                ws.append(w)
            cls.append([-Tl(p, x), -Tl(r, x)] + ws)
            for w in ws: cls.append([-Tl(p, x), Tl(r, x), -w])
            for y in X:
                if y <= x: continue
                cls.append([Tl(p, x), -E(r, x, y), E(p, x, y)]); cls.append([Tl(p, x), E(r, x, y), -E(p, x, y)])
                cls.append([-Tl(p, x), -E(r, x, y), Tl(p, y)]); cls.append([-Tl(p, x), -E(r, x, y), J(p, q, x, y)])
                cls.append([-Tl(p, x), E(r, x, y), -Tl(p, y), -J(p, q, x, y)])
    a, b, c, d, z, w = range(6)
    for (p, q) in [(a, c), (b, c), (b, d), (c, d), (a, z), (b, z)]: join(p, q)
    # matchings: p q p = p and q p q = q
    for (p, q) in [(a, c), (b, c), (b, d)]: product(p, q, p); product(q, p, q)
    product(c, d, z); product(d, c, z); product(a, z, w); product(b, z, w)
    # Case B: z has no T-blocks
    if "--allz" not in sys.argv:
        for x in X: cls.append([-Tl(z, x)])
    if b2:
        for x in X: cls.append([-Tl(a, x), -Tl(b, x)])
    if rank2:
        # exists x,y: t^a_x, t^a_y, not e^a_xy
        sel = []
        for x in X:
            for y in X:
                if x < y:
                    s = pool.id(("sel", x, y)); sel.append(s)
                    cls.append([-s, Tl(a, x)]); cls.append([-s, Tl(a, y)]); cls.append([-s, -E(a, x, y)])
        cls.append(sel)
    # a not matched to d?  (optional: search for counterexample to (S)): if flag
    if "--counter" in sys.argv:
        # elements 6 = a d a, 7 = d a d; require 6 != a or 7 != d
        for p in (6, 7):
            for x, y, zz in itertools.permutations(X, 3):
                if x < zz: cls.append([-E(p, x, y), -E(p, y, zz), E(p, x, zz)])
            for x in X:
                for y in X:
                    if x < y:
                        cls.append([-E(p, x, y), -Tl(p, x), Tl(p, y)]); cls.append([-E(p, x, y), Tl(p, x), -Tl(p, y)])
        join(a, d); product(a, d, 6); product(d, a, 7)
        ds = []
        for (p, q) in ((6, a), (7, d)):
            for x in X:
                dd = pool.id(("dt", p, q, x)); ds.append(dd)
                cls.append([-dd, Tl(p, x), Tl(q, x)]); cls.append([-dd, -Tl(p, x), -Tl(q, x)])
                for y in X:
                    if y <= x: continue
                    dd = pool.id(("de", p, q, x, y)); ds.append(dd)
                    cls.append([-dd, E(p, x, y), E(q, x, y)]); cls.append([-dd, -E(p, x, y), -E(q, x, y)])
        cls.append(ds)
    t = time.time()
    with Cadical153(bootstrap_with=cls) as s:
        ok = s.solve()
        print(f"m={m}: {'SAT' if ok else 'UNSAT'} ({time.time()-t:.0f}s)", flush=True)
        if ok:
            model = set(v for v in s.get_model() if v > 0)
            for p, name in enumerate("abcdzw"):
                blocks = []; seen = set()
                for x in X:
                    if x in seen: continue
                    bl = [x] + [y for y in X if y != x and E(p, x, y) in model]; seen |= set(bl)
                    blocks.append((tuple(bl), 'T' if Tl(p, x) in model else 'N'))
                print("  ", name, blocks)
            return True
    return False
for m in range(3, int(sys.argv[1]) + 1):
    if run(m, b2=("--b1" not in sys.argv and "--any" not in sys.argv), rank2="--norank" not in sys.argv): break
