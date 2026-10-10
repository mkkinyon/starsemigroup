"""Search layered graph semigroups (layered.py) for new obstructions: projection algebras satisfying Q1, the triangle
condition and (S) whose embeddability in P(P_m) is then tested.  Levels sizes (n1, n2, n3) with the bottom complete.
The projection algebra is computed directly: theta_p(q) = p descended to the level f(p,q) at which the descents of
p and q become matched.  Algebras are deduplicated up to isomorphism (canonical form by invariant refinement).
Usage: python3 layered_search.py n1 n2 n3 [M]   (M = largest m tried, default 5); results appended to layered_search.log"""
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
    # invariant refinement (includes the structural bits theta_p(q) = p / = q; iterated until the partition is stable)
    inv = [0] * N; ncl = 1
    while True:
        inv = [hash((inv[p], tuple(sorted((inv[q], inv[A[q][p]], inv[A[p][q]], A[q][p] == p, A[p][q] == q, A[q][p] == q, A[p][q] == p) for q in range(N))))) for p in range(N)]
        n2 = len(set(inv))
        if n2 == ncl or n2 == N: break
        ncl = n2
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

def structures(n1, n2, n3):
    L1 = [f"a{i}" for i in range(n1)]; L2 = [f"b{i}" for i in range(n2)]; L3 = [f"c{i}" for i in range(n3)]
    pairs1 = list(itertools.combinations(L1, 2)); pairs2 = list(itertools.combinations(L2, 2))
    for m2 in range(1 << len(pairs2)):
        E2 = {frozenset(pairs2[t]) for t in range(len(pairs2)) if m2 >> t & 1}
        for m1 in range(1 << len(pairs1)):
            E1 = {frozenset(pairs1[t]) for t in range(len(pairs1)) if m1 >> t & 1}
            for b1 in itertools.product(L2, repeat=n1):
                if set(b1) != set(L2): continue
                bot1 = dict(zip(L1, b1))
                if any(bot1[p] != bot1[q] and frozenset((bot1[p], bot1[q])) not in E2 for p, q in pairs1 if frozenset((p, q)) in E1): continue
                for b2 in itertools.product(L3, repeat=n2):
                    if set(b2) != set(L3): continue
                    bot = dict(bot1); bot.update(zip(L2, b2))
                    yield [L1, L2, L3], E1 | E2, bot

if __name__ == "__main__":
    n1, n2, n3 = map(int, sys.argv[1:4]); M = int(sys.argv[4]) if len(sys.argv) > 4 else 5; MS = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layered_search.log")
    from pa_embed2 import PPm, embed
    Ds = {}
    seen = set(); stats = dict(total=0, q1=0, uniq=0, tri=0, S=0, emb=0, nonemb=0, timeout=0)
    tri_cl = parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)]))
    t0 = time.time()
    for levels, matched, bot in structures(n1, n2, n3):
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
        rec = dict(sizes=[n1, n2, n3], levels=levels, matched=sorted(sorted(x) for x in matched), bot=bot, names=names, A=A, embeds=found)
        with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")
        if not isinstance(found, int): print("CANDIDATE", rec, flush=True)
    print(f"sizes {n1},{n2},{n3}: {stats} ({time.time()-t0:.0f}s)", flush=True)
