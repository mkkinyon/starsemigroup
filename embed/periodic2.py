"""Faster pattern search over periodic projections (see periodic.py): precomputed commutation/
matching tables and dynamic variable ordering (matched partners first)."""
import sys, time, itertools
from periodic import all_elements, Alg, describe, theta

def tables(alg):
    N = len(alg.E); mul = alg.mul
    comm = [dict() for _ in range(N)]     # comm[a][b] = product if a,b commute
    matched = [[] for _ in range(N)]
    t = time.time()
    for a in range(N):
        for b in range(a, N):
            ab = mul(a, b); ba = mul(b, a)
            if ab == ba:
                comm[a][b] = ab; comm[b][a] = ab
            if ab == b and ba == a:
                matched[a].append(b)
                if b != a: matched[b].append(a)
    print(f"tables: {N} elements, {time.time()-t:.0f}s, matched pairs: {sum(len(v) for v in matched)//2}", flush=True)
    return comm, matched

def search(alg, comm, matched, k, edges, maxsol=3, limit=None):
    """variables 0..k-1 = x_1..x_k, k..2k-1 = y_1..y_k"""
    N = len(comm); V = 2 * k
    same = [[b for b in range(V) if b != a and (b < k) == (a < k)] for a in range(V)]   # same side: commute, common product
    partner = [a + k if a < k else a - k for a in range(V)]                              # x_i ~ y_i commute
    match = [set() for _ in range(V)]
    for (i, j) in edges:
        match[i - 1].add(k + j - 1); match[k + j - 1].add(i - 1)
    assign = {}; sols = []; t0 = time.time()
    def candidates(v):
        best = None
        for u in match[v]:
            if u in assign:
                c = matched[assign[u]]
                if best is None or len(c) < len(best): best = c
        return best if best is not None else range(N)
    def consistent(v, c):
        for u in match[v]:
            if u in assign and assign[u] not in matched[c]: return False
        p = partner[v]
        if p in assign and assign[p] not in comm[c]: return False
        prod = None
        for u in same[v]:
            if u in assign:
                if assign[u] not in comm[c]: return False
                q = comm[c][assign[u]]
                if prod is None: prod = q
                elif q != prod: return False
        # common product within the side must also equal products among the already assigned
        if prod is not None:
            side = [assign[u] for u in same[v] if u in assign]
            if len(side) >= 2 and comm[side[0]][side[1]] != prod: return False
        return True
    def rec():
        if limit and time.time() - t0 > limit: raise TimeoutError
        if len(sols) >= maxsol: return
        if len(assign) == V:
            xs = [assign[a] for a in range(k)]; ys = [assign[k + a] for a in range(k)]
            w = comm[xs[0]][xs[1]]; z = comm[ys[0]][ys[1]]
            if w != z: sols.append((xs, ys, w, z))
            return
        # pick variable: most matched-constraints to assigned, then most other constraints
        def score(v):
            return (sum(1 for u in match[v] if u in assign), (partner[v] in assign) + sum(1 for u in same[v] if u in assign))
        v = max((u for u in range(V) if u not in assign), key=score)
        for c in candidates(v):
            if consistent(v, c):
                assign[v] = c; rec(); del assign[v]
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
    which = sys.argv[4:] or list(PATTERNS)
    elems = all_elements(m, pots, mods); alg = Alg(m, elems)
    print(f"m={m}, potentials {pots}, moduli {mods}: {len(elems)} periodic projections", flush=True)
    comm, matched = tables(alg)
    for name in which:
        k, E = PATTERNS[name]; t = time.time()
        status, sols = search(alg, comm, matched, k, E, limit=50000)
        print(f"{name}: {status}, {len(sols)} counterexample(s) ({time.time()-t:.0f}s)", flush=True)
        for xs, ys, w, z in sols[:2]:
            print("   x:", [describe(alg, e) for e in xs]); print("   y:", [describe(alg, e) for e in ys])
            print("   w:", describe(alg, w), "   z:", describe(alg, z), flush=True)
