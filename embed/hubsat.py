"""Abstract SAT search for counterexamples to (S) in the hub case (a class of type (F2)).
Points = edges of a bipartite graph between a-side objects and c-side objects:
  a-side: A_1..A_p (T(a)), B_1..B_p (T(b)), F_1..F_f (common N(a)/N(b) blocks)   [mode B2: S_a = union of A's is an
          N(b)-block, S_b = union of B's is an N(a)-block]
          mode B1: a-side objects are the cells (A_i, B_j) (points of W lie in one A and one B) and F's.
  c-side: C_1..C_p (T(c), union = K = an N(d)-block), D_1..D_p (T(d), union = K' = an N(c)-block), E_1..E_e (common).
Gamma(p,q) is the bipartite graph on the p-blocks and q-blocks with an edge when some point lies in both.
Hypotheses: Gamma(a,c), Gamma(b,c), Gamma(b,d) fine (each component has <=1 T-block of each side, both or none).
Goal: Gamma(a,d) fine.  A SAT answer is a counterexample to (S) (realisable in P_m, m = number of points).
Usage: python3 hubsat.py p f e [B1|B2]"""
import sys, itertools, time
from pysat.solvers import Cadical153
from pysat.formula import IDPool

def run(p, f, e, mode, negate=True):
    pool = IDPool(); cls = []
    A = [f"A{i}" for i in range(p)]; B = [f"B{i}" for i in range(p)]; F = [f"F{i}" for i in range(f)]
    C = [f"C{i}" for i in range(p)]; D = [f"D{i}" for i in range(p)]; E = [f"E{i}" for i in range(e)]
    if mode == "B2":
        aobj = A + B + F
    else:
        aobj = [f"{a}|{b}" for a in A for b in B] + F
    cobj = C + D + E
    def X(u, v): return pool.id(("x", u, v))
    # nonempty blocks: each A, B, C, D, F, E has a point
    def edges_of(objs): return [X(u, v) for u in objs for v in cobj]
    for a in A:
        cls.append([X(u, v) for u in aobj if (u == a or u.startswith(a + "|")) for v in cobj])
    for b in B:
        cls.append([X(u, v) for u in aobj if (u == b or u.endswith("|" + b)) for v in cobj])
    for u in F: cls.append([X(u, v) for v in cobj])
    for v in C + D + E: cls.append([X(u, v) for u in aobj])
    # block classes for each projection
    def ablock(u, proj):   # the block of projection proj (a or b) containing a-side object u
        if u.startswith("F"): return u
        if mode == "B2":
            if proj == "a": return u if u.startswith("A") else "Sb"
            else: return u if u.startswith("B") else "Sa"
        else:
            a, b = u.split("|"); return a if proj == "a" else b
    def cblock(v, proj):
        if v.startswith("E"): return v
        if proj == "c": return v if v.startswith("C") else "Kp"
        else: return v if v.startswith("D") else "K"
    def graph(pa, pc):
        """vertices and adjacency variables of Gamma(pa, pc)"""
        av = sorted({ablock(u, pa) for u in aobj}); cv = sorted({cblock(v, pc) for v in cobj})
        adj = {}
        for x in av:
            for y in cv:
                var = pool.id(("adj", pa, pc, x, y)); adj[(x, y)] = var
                lits = [X(u, v) for u in aobj for v in cobj if ablock(u, pa) == x and cblock(v, pc) == y]
                cls.append([-var] + lits)
                for l in lits: cls.append([var, -l])
        V = av + cv; n = len(V)
        # reachability by doubling; R_k(x,y) symmetric on V
        def R(k, x, y):
            if x > y: x, y = y, x
            return pool.id(("R", pa, pc, k, x, y))
        for x in V:
            for y in V:
                if x < y:
                    r0 = R(0, x, y)
                    if (x in av) != (y in av):
                        a_ = x if x in av else y; c_ = y if x in av else x
                        cls.append([-r0, adj[(a_, c_)]]); cls.append([r0, -adj[(a_, c_)]])
                    else:
                        cls.append([-r0])
        L = max(1, (n - 1).bit_length())
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
        def reach(x, y): return R(L, x, y) if x != y else None
        return av, cv, reach
    def fine(pa, pc, Ta, Tc, negate=False):
        av, cv, reach = graph(pa, pc)
        conds = []   # list of clauses expressing fineness; if negate, we need the disjunction of their negations
        for x, x2 in itertools.combinations(Ta, 2): conds.append([-reach(x, x2)])
        for y, y2 in itertools.combinations(Tc, 2): conds.append([-reach(y, y2)])
        for x in Ta: conds.append([reach(x, y) for y in Tc])
        for y in Tc: conds.append([reach(x, y) for x in Ta])
        if not negate:
            cls.extend(conds)
        else:
            sel = []
            for cl in conds:
                s = pool.id(("neg", pa, pc, tuple(cl))); sel.append(s)
                for l in cl: cls.append([-s, -l])     # s -> clause false
            cls.append(sel)
    fine("a", "c", A, C); fine("b", "c", B, C); fine("b", "d", B, D)
    fine("a", "d", A, D, negate=negate)
    t = time.time()
    with Cadical153(bootstrap_with=cls) as s:
        ok = s.solve()
        print(f"p={p} f={f} e={e} {mode}: {'SAT' if ok else 'UNSAT'} ({time.time()-t:.1f}s, {pool.top} vars)", flush=True)
        if ok:
            model = set(v for v in s.get_model() if v > 0)
            pts = [(u, v) for u in aobj for v in cobj if X(u, v) in model]
            print("   points:", pts)
            return pts
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        for mode in ("B1", "B2"):
            for p in (1, 2, 3):
                for f in range(0, 5):
                    for e in range(0, 5):
                        if run(p, f, e, mode): sys.exit()
    else:
        run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "B2", negate="--sat" not in sys.argv)
