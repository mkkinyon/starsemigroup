"""Search layered graph semigroups (layered.py) for new obstructions: projection algebras satisfying Q1, the triangle
condition and (S) whose embeddability in P(P_m) is then tested.  Levels sizes (n1, n2, n3) with the bottom complete.
The projection algebra is computed directly: theta_p(q) = p descended to the level f(p,q) at which the descents of
p and q become matched.  Algebras are deduplicated up to isomorphism (canonical form by invariant refinement).
Usage: python3 layered_search.py n1,n2,...,nL [M [MS]] [--all]  (backtracking up to m=M, SAT up to m=MS; --all: bot not nec. surjective); results appended to layered_search.log"""
import sys, itertools, json, os, time
from graphsg import q1
from graphsg_survey import s_violations
from digraph import clause, parse_clause, search

def proj_algebra_layered(levels, matched, bot):
    """elements = all vertices of all levels; returns names, table A[x][y] = theta_y(x)"""
    lv = {p: i for i, L in enumerate(levels) for p in L}
    M = set(matched) | {frozenset((p, q)) for p, q in itertools.combinations(levels[-1], 2)}
    def mt(p, q): return p == q or frozenset((p, q)) in M
    def theta(p, q):
        while lv[q] < lv[p]: q = bot[q]
        while lv[p] < lv[q]: p = bot[p]
        while not mt(p, q): p = bot[p]; q = bot[q]
        return p
    names = [p for L in levels for p in L]; idx = {p: i for i, p in enumerate(names)}
    A = [[idx[theta(y, x)] for y in names] for x in names]
    return names, A

def canon(A):
    N = len(A)
    inv = [0] * N
    for _ in range(3):
        new = [hash((inv[p], tuple(sorted((inv[q], inv[A[q][p]], inv[A[p][q]]) for q in range(N))))) for p in range(N)]
        inv = new
    groups = {}
    for p in range(N): groups.setdefault(inv[p], []).append(p)
    keys = sorted(groups)
    best = None
    for perms in itertools.product(*[itertools.permutations(groups[k]) for k in keys]):
        order = [p for perm in perms for p in perm]   # new position i holds old element order[i]
        pos = {p: i for i, p in enumerate(order)}
        tab = tuple(tuple(pos[A[order[x]][order[y]]] for y in range(N)) for x in range(N))
        if best is None or tab < best: best = tab
    return best

def structures(sizes, surjective=True):
    """all layered structures with the given level sizes (labelled): graphs on each level but the last, maps bot
    (surjective if requested) preserving matching"""
    L = len(sizes)
    levels = [[f"{chr(97 + i)}{j}" for j in range(n)] for i, n in enumerate(sizes)]
    pairs = [list(itertools.combinations(Lv, 2)) for Lv in levels]
    def rec(i, E, bot):
        if i == L - 1:
            yield levels, E, bot; return
        for m in range(1 << len(pairs[i])):
            Ei = {frozenset(pairs[i][t]) for t in range(len(pairs[i])) if m >> t & 1}
            for b in itertools.product(levels[i + 1], repeat=sizes[i]):
                if surjective and set(b) != set(levels[i + 1]): continue
                bi = dict(zip(levels[i], b))
                # preservation needs the graph of level i+1 (complete if i+1 == L-1): decided at the next level
                yield from rec2(i, E | Ei, dict(bot, **bi), Ei)
    def rec2(i, E, bot, Ei):
        # choose the graph of level i+1 (or complete bottom) and check that bot preserves Ei
        if i + 1 == L - 1:
            yield levels, E, bot; return
        for m in range(1 << len(pairs[i + 1])):
            Ej = {frozenset(pairs[i + 1][t]) for t in range(len(pairs[i + 1])) if m >> t & 1}
            if any(bot[p] != bot[q] and frozenset((bot[p], bot[q])) not in Ej for p, q in pairs[i] if frozenset((p, q)) in Ei): continue
            for b in itertools.product(levels[i + 2], repeat=sizes[i + 1]):
                if surjective and set(b) != set(levels[i + 2]): continue
                bi = dict(zip(levels[i + 1], b))
                yield from rec2(i + 1, E | Ej, dict(bot, **bi), Ej)
    yield from rec(0, set(), {})

if __name__ == "__main__":
    sizes = [int(a) for a in sys.argv[1].split(',')]; M = int(sys.argv[2]) if len(sys.argv) > 2 else 3; MS = int(sys.argv[3]) if len(sys.argv) > 3 else 8; surj = '--all' not in sys.argv
    LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layered_search.log")
    from pa_embed2 import PPm, embed
    Ds = {}
    seen = set(); stats = dict(total=0, q1=0, uniq=0, tri=0, S=0, emb=0, nonemb=0, timeout=0)
    tri_cl = parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)]))
    t0 = time.time()
    for levels, matched, bot in structures(sizes, surj):
        stats["total"] += 1
        names, A = proj_algebra_layered(levels, matched, bot)
        if not q1(A): continue
        stats["q1"] += 1
        c = canon(A)
        if c in seen: continue
        seen.add(c); stats["uniq"] += 1
        tri = search(tri_cl, range(len(A)), lambda x, y: A[x][y], limit=600) if len(A) >= 6 else []
        if tri: continue
        stats["tri"] += 1
        if s_violations(A): continue
        stats["S"] += 1
        found = None
        for m in range(1, M + 1):
            if m not in Ds: Ds[m] = PPm(m)
            r = embed(A, Ds[m], limit=60)
            if r == "timeout": found = f"timeout@{m}"; break
            if r is not None: found = m; break
        if not isinstance(found, int):
            from pa_sat import solve
            for m in range(M + 1, MS + 1):
                r = solve(A, m, verbose=False)
                if r: found = m; break
        stats["emb" if isinstance(found, int) else ("timeout" if found else "nonemb")] += 1
        rec = dict(sizes=sizes, levels=levels, matched=sorted(sorted(x) for x in matched), bot=bot, names=names, A=A, embeds=found)
        with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")
        if not isinstance(found, int): print("CANDIDATE", rec, flush=True)
    print(f"sizes {sizes}: {stats} ({time.time()-t0:.0f}s)", flush=True)
