"""Exhaustive (type-level) SAT check of the hub case of condition (S).
Inside a class of type (F2): T-blocks A_1..A_p, B_1..B_p (a-side), C_1..C_p, D_1..D_p (c-side), hubs
K = union of C's (an N(d)-block), K' = union of D's (an N(c)-block), and in mode B2 also S_a = union of A's
(an N(b)-block), S_b = union of B's (an N(a)-block); in mode B1 the points of W = union A = union B lie in cells
(A_i, B_j).  Plain N-blocks (common to a,b resp. c,d) form components kappa of the overlap graph; each kappa is
determined, for all four joins, by its touch set (<= 1 block of each of T(a), T(b), T(c), T(d), by fineness),
and kappas with equal touch sets can be merged.  Points with both sides special are direct overlaps.
Variables: presence of each touch type, presence of each direct overlap (and of each cell in mode B1).
Constraints: Gamma(a,c), Gamma(b,c), Gamma(b,d) fine; goal Gamma(a,d) fine negated.  UNSAT for p = 1,2,3
(the only possible p, see the notes) proves the hub case.  Usage: python3 hubtypes.py [p] [B1|B2]"""
import sys, itertools, time
from pysat.solvers import Cadical153, Glucose4, Minisat22
from pysat.formula import IDPool

def run(p, mode, negate=True):
    pool = IDPool(); cls = []
    A = [f"A{i}" for i in range(p)]; B = [f"B{i}" for i in range(p)]; C = [f"C{i}" for i in range(p)]; D = [f"D{i}" for i in range(p)]
    # kappa types: (a, b, c, d) each a block or None, not all None; in B1 a is None iff b is None
    types = []
    for a in A + [None]:
        for b in B + [None]:
            if mode == "B1" and (a is None) != (b is None): continue
            for c in C + [None]:
                for d in D + [None]:
                    if (a, b, c, d) != (None, None, None, None): types.append((a, b, c, d))
    pres = {t: pool.id(("t",) + t) for t in types}
    # direct overlaps: points with both sides special: (a-side object, c-side object)
    aspec = A + B if mode == "B2" else [(a, b) for a in A for b in B]
    cspec = C + D
    over = {(u, v): pool.id(("o", u, v)) for u in aspec for v in cspec}
    cell = {u: pool.id(("cell", u)) for u in aspec} if mode == "B1" else None
    # nonemptiness of T-blocks
    def uses_a(x, t, u): return (t[0] == x) if x.startswith("A") else (t[1] == x)
    for x in A + B:
        lits = [pres[t] for t in types if x in t]
        if mode == "B2": lits += [over[(u, v)] for (u, v) in over if u == x]
        else: lits += [cell[u] for u in aspec if x in u]
        cls.append(lits)
    for y in C + D:
        cls.append([pres[t] for t in types if y in t] + [over[(u, v)] for (u, v) in over if v == y])
    if mode == "B1":
        # a cell is present iff some point lies in it: via a type touching (a,b)?  In B1 a kappa touching A and B does so
        # at a point of the cell (A,B); so type (a,b,*,*) present -> cell (a,b) present; overlap (cell, v) -> cell present.
        for t in types:
            if t[0] is not None: cls.append([-pres[t], cell[(t[0], t[1])]])
        for (u, v) in over: cls.append([-over[(u, v)], cell[u]])
        for u in aspec: cls.append([-cell[u]] + [pres[t] for t in types if (t[0], t[1]) == u] + [over[(u, v)] for v in cspec])
    # block maps
    def ablock(u, proj):
        if mode == "B2":
            if proj == "a": return u if u.startswith("A") else "Sb"
            return u if u.startswith("B") else "Sa"
        return u[0] if proj == "a" else u[1]
    def cblock(v, proj):
        if proj == "c": return v if v.startswith("C") else "Kp"
        return v if v.startswith("D") else "K"
    def graph(pa, pc):
        av = sorted({ablock(u, pa) for u in aspec}); cv = sorted({cblock(v, pc) for v in cspec})
        V = av + cv
        # base adjacency (symmetric) between vertices: R0(x,y)
        def R(k, x, y):
            if x > y: x, y = y, x
            return pool.id(("R", pa, pc, k, x, y))
        for x in V:
            for y in V:
                if x < y:
                    lits = []
                    # direct overlaps
                    for (u, v), var in over.items():
                        if {ablock(u, pa), cblock(v, pc)} == {x, y}: lits.append(var)
                    # types: a type connects all its touched specials' images (through its plain blocks)
                    for t, var in pres.items():
                        imgs = set()
                        if mode == "B2":
                            if t[0] is not None: imgs.add(ablock(t[0], pa))
                            if t[1] is not None: imgs.add(ablock(t[1], pa))
                        elif t[0] is not None: imgs.add(ablock((t[0], t[1]), pa))
                        if t[2] is not None: imgs.add(cblock(t[2], pc))
                        if t[3] is not None: imgs.add(cblock(t[3], pc))
                        if x in imgs and y in imgs: lits.append(var)
                    r0 = R(0, x, y)
                    cls.append([-r0] + lits)
                    for l in lits: cls.append([r0, -l])
        L = max(1, (len(V) - 1).bit_length())
        for k in range(L):
            for x in V:
                for y in V:
                    if x < y:
                        aux = []
                        for u in V:
                            if u in (x, y): continue
                            t = pool.id(("aux", pa, pc, k, x, y, u)); aux.append(t)
                            cls.append([-t, R(k, x, u)]); cls.append([-t, R(k, u, y)]); cls.append([t, -R(k, x, u), -R(k, u, y)])
                        nxt = R(k + 1, x, y)
                        cls.append([-nxt, R(k, x, y)] + aux); cls.append([nxt, -R(k, x, y)])
                        for t in aux: cls.append([nxt, -t])
        return lambda x, y: R(L, x, y)
    def fine(pa, pc, Ta, Tc, negate=False):
        reach = graph(pa, pc); conds = []
        for x, x2 in itertools.combinations(Ta, 2): conds.append([-reach(x, x2)])
        for y, y2 in itertools.combinations(Tc, 2): conds.append([-reach(y, y2)])
        for x in Ta: conds.append([reach(x, y) for y in Tc])
        for y in Tc: conds.append([reach(x, y) for x in Ta])
        if not negate: cls.extend(conds)
        else:
            sel = []
            for cl in conds:
                s = pool.id(("neg", tuple(cl))); sel.append(s)
                for l in cl: cls.append([-s, -l])
            cls.append(sel)
    fine("a", "c", A, C); fine("b", "c", B, C); fine("b", "d", B, D); fine("a", "d", A, D, negate=negate)
    t0 = time.time()
    Solver = {'cadical': Cadical153, 'glucose': Glucose4, 'minisat': Minisat22}[SOLVER]
    with Solver(bootstrap_with=cls) as s:
        ok = s.solve()
        print(f"p={p} {mode}: {'SAT (counterexample!)' if ok else 'UNSAT'} ({time.time()-t0:.1f}s, {pool.top} vars, {len(cls)} clauses)", flush=True)
        if ok:
            m = set(v for v in s.get_model() if v > 0)
            print("  types:", [t for t in types if pres[t] in m]); print("  overlaps:", [k for k, v in over.items() if v in m])
            return True
    return False

SOLVER = "cadical"
if __name__ == "__main__":
    for a in sys.argv:
        if a.startswith("--solver="): SOLVER = a.split("=")[1]
    ps = [int(sys.argv[1])] if len(sys.argv) > 1 and sys.argv[1] != "all" else [1, 2, 3, 4, 5, 6]
    modes = [sys.argv[2]] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else ["B1", "B2"]
    for mode in modes:
        for p in ps: run(p, mode, negate="--sat" not in sys.argv)
