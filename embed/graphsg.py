"""The regular *-semigroups Q(G, bot): top projections = vertices V of a graph G (matching relation:
p |><| q iff p = q or pq is an edge), bottom projections B, bot: V -> B.
Elements: (p,q) for p,q in V (rank 1) and (m,m') for m,m' in B (rank 0), with
  (p,q)(r,s) = (p,s) if q |><| r else (bot p, bot s);  (m,m')(r,s) = (m, bot s);  (p,q)(m,m') = (bot p, m');
  (m,m')(n,n') = (m,n');  (x,y)^* = (y,x).
Projection algebra: theta_p(q) = p if p|><|q else bot(p); theta_p(m) = bot(p); theta_m(x) = m.
Tools: build the semigroup, verify it is a regular *-semigroup, its projection algebra, Q1/triangle checks,
embedding of the projection algebra into P(P_m), and enumeration of all small (G, bot)."""
import sys, itertools, time
from collections import Counter

def semigroup(V, edges, bot, B):
    adj = {v: {v} for v in V}
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    elems = [(p, q) for p in V for q in V] + [(m, n) for m in B for n in B]
    idx = {e: i for i, e in enumerate(elems)}
    top = set(V)
    def mul(x, y):
        p, q = x; r, s = y
        if p in top and q in top and r in top and s in top:
            return (p, s) if r in adj[q] else (bot[p], bot[s])
        pp = p if p in B else bot[p]; ss = s if s in B else bot[s]
        return (pp, ss)
    T = [[idx[mul(x, y)] for y in elems] for x in elems]
    st = [idx[(y, x)] for (x, y) in elems]
    return elems, T, st

def proj_algebra(elems, T, st):
    P = [i for i in range(len(elems)) if st[i] == i and T[i][i] == i]
    loc = {p: k for k, p in enumerate(P)}
    # table x*y = y x y
    return P, [[loc[T[T[y][x]][y]] for y in P] for x in P]

def is_rss(T, st):
    n = len(T)
    return all(T[T[x][y]][z] == T[x][T[y][z]] for x in range(n) for y in range(n) for z in range(n)) and \
           all(st[T[x][y]] == T[st[y]][st[x]] for x in range(n) for y in range(n)) and \
           all(T[T[x][st[x]]][x] == x for x in range(n))

def q1(A):
    N = len(A)
    return all(A[p][q] == A[q][p] for p in range(N) for q in range(N) if any(A[r][p] == r and A[r][q] == r for r in range(N)))

def graphs(k):
    """all graphs on [k] up to isomorphism (small k), as edge lists"""
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    seen = set(); out = []
    for mask in range(1 << len(pairs)):
        E = [pairs[t] for t in range(len(pairs)) if mask >> t & 1]
        key = min(tuple(sorted(tuple(sorted((perm[u], perm[v]))) for u, v in E)) for perm in itertools.permutations(range(k)))
        if key in seen: continue
        seen.add(key); out.append(E)
    return out

if __name__ == "__main__":
    from pa_embed2 import PPm, embed
    from digraph import clause, parse_clause, search
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    Ds = {}
    for k in range(1, kmax + 1):
        V = list(range(k))
        for E in graphs(k):
            # colourings bot: V -> {0..nb-1} up to relabelling of colours and graph automorphisms (crude: canonical by min)
            seen = set()
            for nb in (1, 2, 3):
                if nb > k: continue
                for col in itertools.product(range(nb), repeat=k):
                    if len(set(col)) != nb: continue
                    key = min(tuple(col[perm[i]] for i in range(k)) for perm in itertools.permutations(range(k))
                              if sorted(tuple(sorted((perm[u], perm[v]))) for u, v in E) == sorted(E))
                    # normalise colour names
                    ren = {}; key = tuple(ren.setdefault(c, len(ren)) for c in key)
                    if key in seen: continue
                    seen.add(key)
                    B = [f"m{c}" for c in range(nb)]; bot = {v: f"m{key[v]}" for v in V}
                    elems, T, st = semigroup(V, E, bot, B)
                    assert is_rss(T, st)
                    P, A = proj_algebra(elems, T, st)
                    ok1 = q1(A)
                    tri = [] if len(A) < 6 else search(parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)])), range(len(A)), lambda x, y: A[x][y], limit=600)
                    found = None
                    for m in range(1, M + 1):
                        if m not in Ds: Ds[m] = PPm(m)
                        r = embed(A, Ds[m], limit=600)
                        if r == "timeout": found = ("timeout", m); break
                        if r is not None: found = m; break
                    print(f"k={k} E={E} bot={key}: |Q|={len(elems)}, Q1={ok1}, triangle={'ok' if tri == [] else 'FAILS'}, embeds: {found}", flush=True)
