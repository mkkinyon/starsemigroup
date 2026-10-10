"""Theorem: Q(G, bot) *-embeds in a partition monoid iff bot is a proper colouring and, for every two colours m, n,
the bichromatic subgraph G[V_m, V_n] is a disjoint union of complete bipartite graphs (no induced path a-c-b-d with
bot a = bot b, bot c = bot d).  Necessity: Q1 and (S).  Sufficiency: the explicit rank-1 construction
   X = {x_p : p in V} + {y_C : C a biclique of some G[V_m,V_n]} + {z_m, z'_m : m in B},
   eps_m = blocks {x_q : q in C_n} + {y_C} for every colour n != m and biclique C of G[V_m,V_n], plus {z_m, z'_m},
   m^ = eps_m with all blocks nontransversal;  p^ = eps_{bot p} with the singleton {x_p} transversal;
   (p,q)^ = rank-1 element with upper projection p^ and lower projection q^; (m,m')^ = rank 0, top eps_m, bottom eps_m'.
This script builds the embedding for every (G, bot) with |V| <= K and verifies that it is an injective
*-homomorphism (and that the predicate agrees with the survey log for |V| <= 4).  Usage: python3 graphsg_thm.py K"""
import sys, itertools, json, os
from graphsg import semigroup, is_rss, graphs
from graphsg_survey import colourings
from pmon import canon, mul, star

def bicliques(k, E, bot):
    """for each pair of colours m<n, the connected components of G[V_m,V_n] with >= 1 edge; None if induced P4"""
    adj = {v: set() for v in range(k)}
    for u, v in E: adj[u].add(v); adj[v].add(u)
    cols = sorted(set(bot)); out = []
    for m, n in itertools.combinations(cols, 2):
        Vm = [v for v in range(k) if bot[v] == m]; Vn = [v for v in range(k) if bot[v] == n]
        seen = set()
        for s in Vm:
            if s in seen or not (adj[s] & set(Vn)): continue
            comp = {s}; stack = [s]
            while stack:
                u = stack.pop()
                for w in adj[u]:
                    if bot[w] in (m, n) and w not in comp: comp.add(w); stack.append(w)
            seen |= comp
            Cm = sorted(comp & set(Vm)); Cn = sorted(comp & set(Vn))
            if any(v not in adj[u] for u in Cm for v in Cn): return None   # not complete bipartite: induced P4
            out.append((m, n, Cm, Cn))
    return out

def construct(k, E, bot):
    """returns (N, images) where images maps each element (p,q)/(m,m') of Q(G,bot) to an element of P_N, or None"""
    if any(bot[u] == bot[v] for u, v in E): return None
    bc = bicliques(k, E, bot)
    if bc is None: return None
    cols = sorted(set(bot))
    x = {p: p for p in range(k)}; N = k
    y = {}
    for i, C in enumerate(bc): y[i] = N; N += 1
    z = {}
    for m in cols: z[m] = (N, N + 1); N += 2
    eps = {}
    for m in cols:
        blocks = [[z[m][0], z[m][1]]]
        for i, (m1, n1, Cm, Cn) in enumerate(bc):
            if m == m1: blocks.append([x[q] for q in Cn] + [y[i]])
            elif m == n1: blocks.append([x[q] for q in Cm] + [y[i]])
        used = {v for b in blocks for v in b}
        blocks += [[v] for v in range(N) if v not in used]
        eps[m] = blocks
    def elem(top_blocks, bot_blocks, trans=None):
        """partition of {0..2N-1}: top blocks, bottom blocks (shifted by N); trans = (i, j) joins top point i with bottom j"""
        bl = [list(b) for b in top_blocks] + [[v + N for v in b] for b in bot_blocks]
        if trans:
            i, j = trans
            bi = next(b for b in bl if i in b); bj = next(b for b in bl if j + N in b)
            bl.remove(bi); bl.remove(bj); bl.append(bi + bj)
        return canon(bl)
    img = {}
    for p in range(k):
        for q in range(k): img[(p, q)] = elem(eps[bot[p]], eps[bot[q]], (x[p], x[q]))
    for m in cols:
        for n in cols: img[(f"m{m}", f"m{n}")] = elem(eps[m], eps[n])
    return N, img

def verify(k, E, bot):
    res = construct(k, E, bot)
    if res is None: return None
    N, img = res
    B = [f"m{c}" for c in sorted(set(bot))]; bt = {v: f"m{bot[v]}" for v in range(k)}
    elems, T, st = semigroup(list(range(k)), E, bt, B)
    f = [img[e] for e in elems]
    assert len(set(f)) == len(f), "not injective"
    for i in range(len(elems)):
        assert star(f[i], N) == f[st[i]], "star"
        for j in range(len(elems)):
            assert mul(f[i], f[j], N) == f[T[i][j]], ("hom", elems[i], elems[j])
    return N

if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphsg_survey.log")
    survey = {}
    if os.path.exists(log):
        for l in open(log):
            d = json.loads(l); survey[(d["k"], tuple(map(tuple, d["E"])), tuple(d["bot"]))] = d
    for k in range(1, K + 1):
        tot = emb = 0; maxN = 0
        for E in graphs(k):
            for key in colourings(k, E):
                tot += 1
                N = verify(k, E, key)
                d = survey.get((k, tuple(map(tuple, E)), key))
                if d is not None:
                    assert (N is not None) == isinstance(d["embeds"], int), (k, E, key, N, d)
                if N is not None: emb += 1; maxN = max(maxN, N)
        print(f"k={k}: {tot} coloured graphs, {emb} embeddable (explicit *-embedding verified), max |X| used = {maxN}", flush=True)
