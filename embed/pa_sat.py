"""SAT search for an embedding of a finite projection algebra (table T[x][y] = y x y) into P(P_m).
Points X = [m]; each element p is an equivalence relation e^p on X with a T-label per point.
theta_p(q) = p q p is computed pointwise from the join J^{pq} (encoded by m-1 rounds of path extension).
Usage: python3 pa_sat.py m  [--table "..."]   (default: the 6-element algebra M172)"""
import sys, itertools, time, json
from pysat.solvers import Cadical153
from pysat.formula import IDPool

def solve(T, m, distinct=True, verbose=True, timeout=None, symbreak=True, extra=None):
    k = len(T); pool = IDPool(); cls = []
    X = range(m)
    def E(p, x, y):
        if x == y: return None
        if x > y: x, y = y, x
        return pool.id(("e", p, x, y))
    def Tl(p, x): return pool.id(("t", p, x))
    def J(p, q, x, y):
        if p > q: p, q = q, p
        if x > y: x, y = y, x
        return pool.id(("J", p, q, x, y))
    # equivalence relations and label consistency
    for p in range(k):
        for x, y, z in itertools.permutations(X, 3):
            if x < z:
                cls.append([-E(p, x, y), -E(p, y, z), E(p, x, z)])
        for x in X:
            for y in X:
                if x < y:
                    cls.append([-E(p, x, y), -Tl(p, x), Tl(p, y)]); cls.append([-E(p, x, y), Tl(p, x), -Tl(p, y)])
    # joins for all pairs p < q used in some product (all pairs)
    pairs = sorted({(min(x, y), max(x, y)) for x in range(k) for y in range(k) if x != y})
    for (p, q) in pairs:
        # R_0 = e^p or e^q ; R_{i+1}(x,y) <-> R_i(x,y) or exists u: R_i(x,u) & R_0(u,y)
        def R(i, x, y):
            if x > y: x, y = y, x
            return pool.id(("R", p, q, i, x, y))
        for x in X:
            for y in X:
                if x < y:
                    r0 = R(0, x, y)
                    cls.append([-r0, E(p, x, y), E(q, x, y)]); cls.append([r0, -E(p, x, y)]); cls.append([r0, -E(q, x, y)])
        L = max(1, (m - 1).bit_length())   # doubling: R_{i+1} = R_i o R_i suffices after log2 rounds
        for i in range(L):
            for x in X:
                for y in X:
                    if x < y:
                        # R_{i+1}(x,y) <-> R_i(x,y) or OR_u (R_i(x,u) & R_i(u,y))
                        aux = []
                        for u in X:
                            if u in (x, y): continue
                            a = pool.id(("aux", p, q, i, x, y, u))
                            cls.append([-a, R(i, x, u)]); cls.append([-a, R(i, u, y)]); cls.append([a, -R(i, x, u), -R(i, u, y)])
                            aux.append(a)
                        nxt = R(i + 1, x, y)
                        cls.append([-nxt, R(i, x, y)] + aux)
                        cls.append([nxt, -R(i, x, y)])
                        for a in aux: cls.append([nxt, -a])
        for x in X:
            for y in X:
                if x < y:
                    cls.append([-J(p, q, x, y), R(L, x, y)]); cls.append([J(p, q, x, y), -R(L, x, y)])
    # products: r = theta_p(q) = p q p = T[q][p]
    for p in range(k):
        for q in range(k):
            if p == q: continue
            r = T[q][p]
            if r is None: continue   # relation not imposed
            for x in X:
                # label of x in r
                # if not t^p_x: not t^r_x ; if t^p_x: t^r_x <-> exists y (J(x,y) or y==x) & t^q_y
                cls.append([Tl(p, x), -Tl(r, x)])
                ws = []
                for y in X:
                    if y == x:
                        w = pool.id(("w", p, q, x, y)); cls.append([-w, Tl(q, y)]); cls.append([w, -Tl(q, y)])
                    else:
                        w = pool.id(("w", p, q, x, y)); cls.append([-w, J(p, q, x, y)]); cls.append([-w, Tl(q, y)]); cls.append([w, -J(p, q, x, y), -Tl(q, y)])
                    ws.append(w)
                cls.append([-Tl(p, x), -Tl(r, x)] + ws)
                for w in ws: cls.append([-Tl(p, x), Tl(r, x), -w])
                for y in X:
                    if y <= x: continue
                    # if not t^p_x: e^r_xy <-> e^p_xy
                    cls.append([Tl(p, x), -E(r, x, y), E(p, x, y)]); cls.append([Tl(p, x), E(r, x, y), -E(p, x, y)])
                    # if t^p_x: e^r_xy <-> t^p_y & J_xy
                    cls.append([-Tl(p, x), -E(r, x, y), Tl(p, y)]); cls.append([-Tl(p, x), -E(r, x, y), J(p, q, x, y)])
                    cls.append([-Tl(p, x), E(r, x, y), -Tl(p, y), -J(p, q, x, y)])
    # distinctness
    if distinct:
        pairs_d = [(p, q) for p in range(k) for q in range(p + 1, k)] if distinct is True else list(distinct)
        for (p, q) in pairs_d:
            if True:
                ds = []
                for x in X:
                    d = pool.id(("dt", p, q, x)); ds.append(d)
                    cls.append([-d, Tl(p, x), Tl(q, x)]); cls.append([-d, -Tl(p, x), -Tl(q, x)])
                    for y in X:
                        if y <= x: continue
                        d = pool.id(("de", p, q, x, y)); ds.append(d)
                        cls.append([-d, E(p, x, y), E(q, x, y)]); cls.append([-d, -E(p, x, y), -E(q, x, y)])
                cls.append(ds)
    if symbreak:
        # point 0 lies in a T-block of element 0 only if ... (mild): points ordered by label of element 0
        for x in range(m - 1):
            cls.append([Tl(0, x), -Tl(0, x + 1)])
    if extra is not None: extra(pool, E, Tl, J, cls, X)   # user clauses, e.g. block-level statements to refute
    if verbose: print(f"m={m}: {pool.top} variables, {len(cls)} clauses", flush=True)
    import os
    if os.environ.get('PA_SAT_DUMP'):      # write the CNF (DIMACS) for an external solver instead of solving; counts as UNSAT
        from pysat.formula import CNF
        k_ = int(os.environ.get('PA_SAT_DUMP_N', '0')) + 1; os.environ['PA_SAT_DUMP_N'] = str(k_)
        path = f"{os.environ['PA_SAT_DUMP']}_{k_}.cnf"; CNF(from_clauses=cls).to_file(path)
        print(f"dumped {path}: {pool.top} variables, {len(cls)} clauses (m={m})", flush=True)
        return None
    t = time.time()
    with Cadical153(bootstrap_with=cls) as s:
        ok = s.solve()
        if verbose: print(f"   {'SAT' if ok else 'UNSAT'} ({time.time()-t:.0f}s)", flush=True)
        if ok:
            model = set(v for v in s.get_model() if v > 0)
            out = []
            for p in range(k):
                blocks = []; seen = set()
                for x in X:
                    if x in seen: continue
                    b = [x] + [y for y in X if y != x and E(p, x, y) in model]
                    seen |= set(b); blocks.append((tuple(b), 'T' if Tl(p, x) in model else 'N'))
                out.append(blocks)
            return out
    return None

M172 = [[0,0,0,3,3,3],[0,1,0,3,3,5],[0,0,2,3,4,5],[0,0,0,3,3,3],[0,0,2,3,4,3],[0,1,2,3,3,5]]

if __name__ == "__main__":
    m = int(sys.argv[1])
    T = json.loads(sys.argv[sys.argv.index("--table") + 1]) if "--table" in sys.argv else M172
    r = solve(T, m)
    if r:
        for p, blocks in enumerate(r): print(p, blocks)
