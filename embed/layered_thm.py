"""Theorem (layered graph semigroups): Q(V) *-embeds in a partition monoid iff (i) distinct matched elements lie in
different trees (this is Q1) and (ii) for every level and every two trees the bipartite graph of matchings between
their nodes on that level is a disjoint union of complete bipartite graphs (this is (S), given (i)).
Construction: X = {x_v : v not a root} + {y_C : C a biclique} + {z_T, z'_T : T a tree};
  eps_T has the blocks {y_C} + {x_u : u in C, u not in T} for the bicliques C touching T, the pair {z_T, z'_T},
  singletons otherwise;  p^ = eps_{T(p)} with the chain points x_{p_j} (lv p <= j < L) marked transversal;
  (p,q)^ = upper p^, lower q^, transversal blocks {x_{p_j}, x'_{q_j}}.
This script checks the predicate against layered_search.log and verifies the construction (injective
*-homomorphism of the whole semigroup) on every structure in the log and on random structures.
Usage: python3 layered_thm.py [ntrials]"""
import sys, json, os, itertools, random
from layered import build, random_structure, bot_preserves
from graphsg import is_rss, q1
from pmon import canon, mul, star

def analyse(levels, matched, bot):
    """returns (ok, trees, bicliques) where ok = predicate (i)&(ii); trees: node -> root"""
    L = len(levels); lv = {p: i for i, Lv in enumerate(levels) for p in Lv}
    M = set(matched) | {frozenset((p, q)) for p, q in itertools.combinations(levels[-1], 2)}
    def root(p):
        while lv[p] < L - 1: p = bot[p]
        return p
    tree = {p: root(p) for Lv in levels for p in Lv}
    # (i)
    for e in M:
        p, q = tuple(e)
        if lv[p] != lv[q]: return None
        if tree[p] == tree[q] and lv[p] < L - 1: return False, tree, None
    # (ii): per level < L-1 and pair of trees, components of the bipartite matching graph must be complete bipartite
    bicl = []
    for i, Lv in enumerate(levels[:-1]):
        for r1, r2 in itertools.combinations(sorted(set(tree[p] for p in Lv)), 2):
            nodes = [p for p in Lv if tree[p] in (r1, r2)]
            adj = {p: {q for q in nodes if q != p and frozenset((p, q)) in M and tree[q] != tree[p]} for p in nodes}
            seen = set()
            for s in nodes:
                if s in seen or not adj[s]: continue
                comp = {s}; stack = [s]
                while stack:
                    u = stack.pop()
                    for w in adj[u]:
                        if w not in comp: comp.add(w); stack.append(w)
                seen |= comp
                A = sorted(u for u in comp if tree[u] == r1); B = sorted(u for u in comp if tree[u] == r2)
                if any(b not in adj[a] for a in A for b in B): return False, tree, None
                bicl.append((i, r1, r2, A, B))
    return True, tree, bicl

def construct(levels, matched, bot):
    res = analyse(levels, matched, bot)
    if not res or not res[0]: return None
    _, tree, bicl = res
    L = len(levels); lv = {p: i for i, Lv in enumerate(levels) for p in Lv}
    roots = levels[-1]
    x = {}; N = 0
    for Lv in levels[:-1]:
        for v in Lv: x[v] = N; N += 1
    y = {}
    for k, C in enumerate(bicl): y[k] = N; N += 1
    z = {}
    for r in roots: z[r] = (N, N + 1); N += 2
    eps = {}
    for r in roots:
        blocks = [[z[r][0], z[r][1]]]
        for k, (i, r1, r2, A, B) in enumerate(bicl):
            if r == r1: blocks.append([x[u] for u in B] + [y[k]])
            elif r == r2: blocks.append([x[u] for u in A] + [y[k]])
        used = {v for b in blocks for v in b}
        blocks += [[v] for v in range(N) if v not in used]
        eps[r] = blocks
    def chain(p):
        out = []
        while lv[p] < L - 1: out.append(p); p = bot[p]
        return out
    def elem(p, q):
        bl = [list(b) for b in eps[tree[p]]] + [[v + N for v in b] for b in eps[tree[q]]]
        for u, w in zip(chain(p), chain(q)):
            bu = next(b for b in bl if x[u] in b); bw = next(b for b in bl if x[w] + N in b)
            bl.remove(bu); bl.remove(bw); bl.append(bu + bw)
        return canon(bl)
    img = {}
    for Lv in levels:
        for p in Lv:
            for q in Lv: img[(p, q)] = elem(p, q)
    return N, img

def verify(levels, matched, bot):
    res = construct(levels, matched, bot)
    if res is None: return None
    N, img = res
    elems, T, st = build(levels, matched, bot)
    f = [img[e] for e in elems]
    assert len(set(f)) == len(f), "not injective"
    for i in range(len(elems)):
        assert star(f[i], N) == f[st[i]], "star"
        for j in range(len(elems)):
            assert mul(f[i], f[j], N) == f[T[i][j]], ("hom", elems[i], elems[j])
    return N

if __name__ == "__main__":
    log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layered_search.log")
    n = 0
    if os.path.exists(log):
        for line in open(log):
            d = json.loads(line)
            levels = d["levels"]; matched = {frozenset(e) for e in d["matched"]}; bot = d["bot"]
            N = verify(levels, matched, bot)
            assert (N is not None) == isinstance(d["embeds"], int), d
            n += 1
    print(f"log: {n} structures, construction verified on all embeddable ones, predicate agrees with the search")
    # random structures: predicate (i)&(ii) vs Q1 & (S) on the projection algebra
    from layered_search import proj_algebra_layered
    from graphsg_survey import s_violations
    random.seed(7); trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    cnt = {}
    for t in range(trials):
        sizes = [random.randint(1, 4), random.randint(1, 3), random.randint(1, 3), random.randint(1, 2)][: random.randint(2, 4)]
        levels, matched, bot = random_structure(sizes, edge_prob=random.choice([0.2, 0.5, 0.8]))
        if not bot_preserves(levels, matched, bot): continue
        names, A = proj_algebra_layered(levels, matched, bot)
        pred = analyse(levels, matched, bot)[0]
        cond = q1(A) and s_violations(A) == 0
        assert pred == cond, (levels, matched, bot)
        if pred:
            N = verify(levels, matched, bot); cnt["embedded"] = cnt.get("embedded", 0) + 1
        else: cnt["not"] = cnt.get("not", 0) + 1
    print("random trials:", cnt, "(predicate == Q1 & (S) in every case; construction verified when it holds)")
