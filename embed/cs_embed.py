"""Explicit embedding of a completely simple regular *-semigroup M[G;I,I;P] (normal form) into P_X.
G <= Sym(k) given by permutations of range(k); P[i][j] in G with P[i][i]=id, P[j][i]=P[i][j]^{-1}.
X = {a(i,s)} u {c(i,j,s)} for i != j, s in range(k)."""
import sys, itertools
sys.path.insert(0, '..')
from pmon import canon, mul, star as pstar, rank

def build(G, I, P, k):
    # points
    pts = {}
    def pt(key):
        if key not in pts: pts[key] = len(pts)
        return pts[key]
    for i in I:
        for s in range(k): pt(('a', i, s))
    for i in I:
        for j in I:
            if i != j:
                for s in range(k): pt(('c', i, j, s))
    n = len(pts)
    comp = lambda p, q: tuple(p[q[t]] for t in range(k))   # p after q
    inv = lambda p: tuple(sorted(range(k), key=lambda t: p[t]))
    def element(i, g, j):
        """(i,g,j): transversal blocks a(i,s) -- a(j, g(s))' ; N-blocks as in the construction."""
        blocks = []
        for s in range(k):
            blocks.append([pt(('a', i, s)), n + pt(('a', j, g[s]))])
        # upper N-blocks: those of p_i ; lower N-blocks: those of p_j
        def nblocks(i):
            res = []
            for l in I:
                if l == i: continue
                for s in range(k):
                    t = P[i][l][s]      # p_il(s)
                    res.append([pt(('c', i, l, s)), pt(('a', l, t)), pt(('c', l, i, t))])
            # connectors c(l,m,s) with i not in {l,m}: singletons
            for l in I:
                for m in I:
                    if l != m and i not in (l, m):
                        for s in range(k): res.append([pt(('c', l, m, s))])
            return res
        for b in nblocks(i): blocks.append(b)
        for b in nblocks(j): blocks.append([n + x for x in b])
        return canon(blocks)
    return element, n

if __name__ == "__main__":
    # example: G = Z_3 as regular permutation representation on 3 points, I = 3 rows, nonflat P
    k = 3
    Z3 = [(0,1,2), (1,2,0), (2,0,1)]
    comp = lambda p, q: tuple(p[q[t]] for t in range(k)); inv = lambda p: tuple(sorted(range(k), key=lambda t: p[t]))
    t = Z3[1]
    I = [0, 1, 2]
    P = [[Z3[0], t, Z3[0]], [inv(t), Z3[0], Z3[0]], [Z3[0], Z3[0], Z3[0]]]
    element, n = build(Z3, I, P, k)
    elems = {(i, g, j): element(i, g, j) for i in I for g in Z3 for j in I}
    print("|X| =", n, "; elements:", len(elems), "; distinct images:", len(set(elems.values())))
    ok = True
    for (i, g, j), x in elems.items():
        assert pstar(x, n) == elems[(j, inv(g), i)]
        for (l, h, m), y in elems.items():
            prod = elems[(i, comp(comp(g, P[j][l]), h), m)]
            if mul(x, y, n) != prod: ok = False
    print("homomorphism & involution check:", ok)
    print("rank of images:", {rank(x, n) for x in elems.values()})
