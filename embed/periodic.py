"""Periodic projections of the partition monoid P_X, X = Z x [m], invariant under the level shift
(n,i) -> (n+1,i), and exhaustive search for matching-pattern counterexamples among them.

A periodic partition of Z x [m] is given by a partition of [m] into 'types' c, each with a modulus
d_c >= 0 and a potential phi_c : c -> Z (mod d_c if d_c > 0), up to an additive constant:
   d_c = 0 : finite blocks  B_n = {(n + phi(i), i) : i in c},  n in Z;
   d_c > 0 : d_c infinite blocks  B_r = {(n, i) : i in c, n = phi(i) + r (mod d_c)}.
A periodic projection is a periodic partition with a T/N label per type (shift-invariant).
Products are computed exactly via Lemma PX(a): the blocks of theta_p(q) = p q p are the N(p)-blocks
and the sets U_K (union of the T(p)-blocks in a class K of eps_p v eps_q meeting supp p),
U_K being a T-block iff K meets supp q.  Joins of periodic partitions are computed with a weighted
union-find on [m] (voltage graph), tracking the monodromy (modulus) of each component.
"""
import itertools, sys, time, re
from math import gcd
from functools import lru_cache

# ---------- elements ----------
# element = tuple of types; type = (nodes(tuple, sorted), d, pots(tuple, aligned with nodes, normalised), label 'T'/'N')

def normalise_type(nodes, d, pots, label):
    nodes = tuple(sorted(nodes))
    base = pots[nodes[0]]
    if d > 0:
        p = tuple((pots[i] - base) % d for i in nodes)
    else:
        p = tuple(pots[i] - base for i in nodes)
    return (nodes, d, p, label)

def make_element(types):
    return tuple(sorted(types))

def edges_of(elem):
    """voltage edges (i, j, v): (n,i) ~ (n+v, j); loops (i,i,d) for infinite types"""
    E = []
    for nodes, d, pots, lab in elem:
        for a in range(1, len(nodes)):
            E.append((nodes[0], nodes[a], pots[a] - pots[0]))
        if d > 0:
            E.append((nodes[0], nodes[0], d))
    return E

class WUF:
    def __init__(self, m):
        self.par = list(range(m)); self.off = [0] * m; self.mod = [0] * m
    def find(self, i):
        # returns (root, potential of i relative to root)
        path = []
        while self.par[i] != i:
            path.append(i); i = self.par[i]
        root = i; acc = 0
        for j in reversed(path):
            acc += self.off[j]; self.off[j] = acc; self.par[j] = root
        # recompute: after compression each node's off is relative to root
        # (acc accumulated from the top: reversed(path) goes from nearest-to-root outward)
        return root
    def pot(self, i):
        r = self.find(i)
        return r, (0 if i == r else self.off[i])
    def union(self, i, j, v):   # pot(j) = pot(i) + v
        ri, pi = self.pot(i); rj, pj = self.pot(j)
        if ri == rj:
            disc = abs(pi + v - pj)
            if disc: self.mod[ri] = gcd(self.mod[ri], disc)
        else:
            # attach rj under ri: pot(rj) rel ri = pi + v - pj
            self.par[rj] = ri; self.off[rj] = pi + v - pj
            self.mod[ri] = gcd(self.mod[ri], self.mod[rj])

def components(m, edges):
    """components of the voltage graph: list of (nodes set, modulus, pots dict)"""
    uf = WUF(m)
    for i, j, v in edges: uf.union(i, j, v)
    comps = {}
    for i in range(m):
        r, p = uf.pot(i)
        comps.setdefault(r, {})[i] = p
    out = []
    for r, pots in comps.items():
        out.append((frozenset(pots), uf.mod[r], pots))
    return out

def theta(p, q, m):
    """theta_p(q) = p q p as a periodic projection"""
    edges = edges_of(p) + edges_of(q)
    comps = components(m, edges)
    # which join component contains each type of p and q
    Ttypes_q = [set(t[0]) for t in q if t[3] == 'T']
    new = []
    for nodes, d, pots, lab in p:
        if lab == 'N':
            new.append((nodes, d, pots, lab))
    for K, g, psi in comps:
        Tp = [t for t in p if t[3] == 'T' and set(t[0]) <= K]
        if not Tp: continue
        U = sorted(set().union(*[set(t[0]) for t in Tp]))
        label = 'T' if any(tq <= K for tq in Ttypes_q) else 'N'
        new.append(normalise_type(U, g, psi, label))
    return make_element(new)

# ---------- enumeration ----------
def set_partitions(items):
    items = list(items)
    if not items:
        yield []
        return
    first = items[0]
    for rest in set_partitions(items[1:]):
        for k in range(len(rest)):
            yield rest[:k] + [[first] + rest[k]] + rest[k + 1:]
        yield [[first]] + rest

def all_elements(m, pot_range=(-1, 0, 1), moduli=(0, 1, 2), labels=('T', 'N')):
    elems = set()
    for part in set_partitions(range(m)):
        per_type = []
        for c in part:
            c = sorted(c); opts = []
            for d in moduli:
                rel = list(itertools.product(pot_range, repeat=len(c) - 1))
                if d > 0:
                    rel = list({tuple(x % d for x in r) for r in rel})
                for r in rel:
                    pots = {c[0]: 0}
                    for a, i in enumerate(c[1:]): pots[i] = r[a]
                    for lab in labels:
                        opts.append(normalise_type(c, d, pots, lab))
            per_type.append(opts)
        for combo in itertools.product(*per_type):
            elems.add(make_element(combo))
    return sorted(elems)

# ---------- search ----------
class Alg:
    def __init__(self, m, elems):
        self.m = m; self.E = elems; self.idx = {e: k for k, e in enumerate(elems)}
        self.cache = {}; self.nocache = False
    def mul(self, x, y):
        """x*y = theta_y(x), on indices; result index (elements outside the enumerated set get new indices)"""
        key = (x, y)
        r = self.cache.get(key)
        if r is None:
            e = theta(self.E[y], self.E[x], self.m)
            r = self.idx.get(e)
            if r is None:
                r = len(self.E); self.E.append(e); self.idx[e] = r
            if not self.nocache: self.cache[key] = r
        return r

def search(alg, k, edges, limit=None, distinct=False, maxsol=5):
    """pattern condition for digraph `edges` on [k]: find x_1..x_k, y_1..y_k with
    x_i x_j = x_j x_i = w, y_i y_j = y_j y_i = z, x_i y_i = y_i x_i, x_i |><| y_j for edges, w != z.
    Variables are chosen in the order x_1..x_k, y_1..y_k with incremental checks."""
    N0 = len(alg.E); mul = alg.mul; dom = range(N0)
    sols = []; t0 = time.time()
    def matched(p, q): return mul(q, p) == p and mul(p, q) == q
    def rec_x(i, xs, w):
        if limit and time.time() - t0 > limit: raise TimeoutError
        if i == k:
            rec_y(0, xs, w, [], None); return
        for c in dom:
            if distinct and c in xs: continue
            ok = True; w2 = w
            for a in xs:
                u = mul(a, c)
                if u != mul(c, a): ok = False; break
                if w2 is None: w2 = u
                elif u != w2: ok = False; break
            if ok: rec_x(i + 1, xs + [c], w2)
    def rec_y(j, xs, w, ys, z):
        if len(sols) >= maxsol: return
        if j == k:
            if w != z: sols.append((list(xs), list(ys), w, z))
            return
        for c in dom:
            if distinct and c in ys: continue
            if mul(xs[j], c) != mul(c, xs[j]): continue
            ok = True; z2 = z
            for b in ys:
                u = mul(b, c)
                if u != mul(c, b): ok = False; break
                if z2 is None: z2 = u
                elif u != z2: ok = False; break
            if not ok: continue
            # matchings involving y_{j+1} = c with already chosen x's
            if any(not matched(xs[i - 1], c) for (i, jj) in edges if jj == j + 1): continue
            rec_y(j + 1, xs, w, ys + [c], z2)
    try:
        rec_x(0, [], None)
    except TimeoutError:
        return "timeout", sols
    return "done", sols

def describe(alg, e):
    return " | ".join(f"{list(n)}{'/'+str(d) if d else ''} phi={list(p)} {lab}" for n, d, p, lab in alg.E[e])

PATTERNS = {
    "single edge {12} (k=3, star: expect counterexamples)": (3, [(1, 2)]),
    "triangle (k=3, Theorem 4.1: expect none)": (3, [(1, 2), (2, 3), (3, 1)]),
    "hexagon (k=3, expect none)": (3, [(i, j) for i in range(1, 4) for j in range(1, 4) if i != j]),
    "path {12,23} (k=3, OPEN)": (3, [(1, 2), (2, 3)]),
    "2-cycle {12,21} (k=3, OPEN)": (3, [(1, 2), (2, 1)]),
    "disjoint {12,34} (k=4, OPEN)": (4, [(1, 2), (3, 4)]),
}

if __name__ == "__main__":
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    pots = tuple(int(v) for v in sys.argv[2].split(",")) if len(sys.argv) > 2 else (-1, 0, 1)
    mods = tuple(int(v) for v in sys.argv[3].split(",")) if len(sys.argv) > 3 else (0, 1, 2)
    which = sys.argv[4:] if len(sys.argv) > 4 else list(PATTERNS)
    elems = all_elements(m, pots, mods)
    alg = Alg(m, elems)
    print(f"m={m}, potentials {pots}, moduli {mods}: {len(elems)} periodic projections", flush=True)
    for name in which:
        for key, (k, E) in PATTERNS.items():
            if name in key or name == key:
                t = time.time()
                status, sols = search(alg, k, E, limit=20000)
                print(f"{key}: {status}, {len(sols)} counterexample(s) found ({time.time()-t:.0f}s)", flush=True)
                for xs, ys, w, z in sols[:2]:
                    print("   x:", [describe(alg, e) for e in xs]); print("   y:", [describe(alg, e) for e in ys])
                    print("   w:", describe(alg, w)); print("   z:", describe(alg, z))
