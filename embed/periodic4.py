"""Pattern search over periodic projections with indexed candidate sets:
prodmap[(a,p)] = {b : a,b commute with product p}, matched[a] = {b : a |><| b}, comm[a] = {b : a,b commute}."""
import sys, time
from collections import defaultdict
from periodic import all_elements, Alg, describe

def tables(alg):
    N = len(alg.E); mul = alg.mul
    comm = [set() for _ in range(N)]; prod = {}; matched = [set() for _ in range(N)]
    prodmap = defaultdict(set)
    t = time.time()
    for a in range(N):
        for b in range(a, N):
            ab = mul(a, b); ba = mul(b, a)
            if ab == ba:
                comm[a].add(b); comm[b].add(a); prod[(a, b)] = ab; prod[(b, a)] = ab
                prodmap[(a, ab)].add(b); prodmap[(b, ab)].add(a)
            if ab == b and ba == a:
                matched[a].add(b); matched[b].add(a)
    print(f"tables: {N} elements, {time.time()-t:.0f}s, matched pairs: {sum(len(v) for v in matched)//2}, commuting pairs: {len(prod)//2}", flush=True)
    return comm, prod, matched, prodmap

def search(alg, T, k, edges, maxsol=3, limit=None, progress=False, transport=True):
    comm, prod, matched, prodmap = T
    mul = alg.mul
    N = len(comm); V = 2 * k
    same = [[b for b in range(V) if b != a and (b < k) == (a < k)] for a in range(V)]
    partner = [a + k if a < k else a - k for a in range(V)]
    match = [set() for _ in range(V)]
    for (i, j) in edges:
        match[i - 1].add(k + j - 1); match[k + j - 1].add(i - 1)
    assign = {}; sols = []; t0 = time.time(); count = [0]
    def candidates(v):
        cands = None
        for u in match[v]:
            if u in assign:
                s = matched[assign[u]]; cands = s if cands is None else cands & s
        # same-side product constraints
        side = [assign[u] for u in same[v] if u in assign]
        if side:
            p = prod[(side[0], side[1])] if len(side) >= 2 else None
            if p is None:
                s = comm[side[0]]; cands = s if cands is None else cands & s
            else:
                for a in side:
                    s = prodmap.get((a, p), set()); cands = s if cands is None else cands & s
        if partner[v] in assign:
            s = comm[assign[partner[v]]]; cands = s if cands is None else cands & s
        return range(N) if cands is None else cands
    def consistent(v, c):
        side = [assign[u] for u in same[v] if u in assign]
        if len(side) == 1:
            return True   # product will be fixed by this pair
        return True
    nonisolated = {i - 1 for e in edges for i in e}
    def derived_ok():
        # transport relations (Theorem 4.11(a)) at every non-isolated index, and w |><| z
        xs = [assign.get(a) for a in range(k)]; ys = [assign.get(k + a) for a in range(k)]
        ax = [a for a in xs if a is not None]; by = [b for b in ys if b is not None]
        w = prod[(ax[0], ax[1])] if len(ax) >= 2 else None
        z = prod[(by[0], by[1])] if len(by) >= 2 else None
        if w is not None and z is not None:
            if mul(w, z) != z or mul(z, w) != w: return False        # z w z = z, w z w = w
        for i in nonisolated:
            xi, yi = xs[i], ys[i]
            if xi is not None and yi is not None:
                mi = prod[(xi, yi)]
                if w is not None and (mul(w, yi) != mi or mul(yi, w) != w): return False    # b_i w b_i = m_i, w b_i w = w
                if z is not None and (mul(z, xi) != mi or mul(xi, z) != z): return False    # a_i z a_i = m_i, z a_i z = z
        return True
    def rec():
        if limit and time.time() - t0 > limit: raise TimeoutError
        if len(sols) >= maxsol: return
        if transport and not derived_ok(): return
        if len(assign) == V:
            xs = [assign[a] for a in range(k)]; ys = [assign[k + a] for a in range(k)]
            w = prod[(xs[0], xs[1])]; z = prod[(ys[0], ys[1])]
            if w != z: sols.append((xs, ys, w, z))
            return
        def score(v):
            return (sum(1 for u in match[v] if u in assign), (partner[v] in assign) + sum(1 for u in same[v] if u in assign))
        v = max((u for u in range(V) if u not in assign), key=score)
        for c in candidates(v):
            assign[v] = c
            if len(assign) == 1:
                count[0] += 1
                if progress and count[0] % 100 == 0: print(f"   ... first variable {count[0]}/{N} ({time.time()-t0:.0f}s)", flush=True)
            rec(); del assign[v]
            if len(sols) >= maxsol: return
    try:
        rec()
    except TimeoutError:
        return "timeout", sols
    return "done", sols

PATTERNS = {
    "single": (3, [(1, 2)]),
    "triangle": (3, [(1, 2), (2, 3), (3, 1)]),
    "hexagon": (3, [(i, j) for i in range(1, 4) for j in range(1, 4) if i != j]),
    "path": (3, [(1, 2), (2, 3)]),
    "2cycle": (3, [(1, 2), (2, 1)]),
    "disjoint": (4, [(1, 2), (3, 4)]),
    "K22": (4, [(1, 3), (1, 4), (2, 3), (2, 4)]),
    "C4": (4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
}

if __name__ == "__main__":
    m = int(sys.argv[1]); pots = tuple(int(v) for v in sys.argv[2].split(",")); mods = tuple(int(v) for v in sys.argv[3].split(","))
    which = [a for a in sys.argv[4:] if not a.startswith("--")] or list(PATTERNS)
    elems = all_elements(m, pots, mods); alg = Alg(m, elems); alg.nocache = "--nocache" in sys.argv
    print(f"m={m}, potentials {pots}, moduli {mods}: {len(elems)} periodic projections", flush=True)
    T = tables(alg)
    for name in which:
        k, E = PATTERNS[name]; t = time.time()
        status, sols = search(alg, T, k, E, limit=200000, progress=True, transport=(name not in ("single",)))
        print(f"{name}: {status}, {len(sols)} counterexample(s) ({time.time()-t:.0f}s)", flush=True)
        for xs, ys, w, z in sols[:2]:
            print("   x:", [describe(alg, e) for e in xs]); print("   y:", [describe(alg, e) for e in ys])
            print("   w:", describe(alg, w), "   z:", describe(alg, z), flush=True)
