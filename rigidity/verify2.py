"""
Verification for the description of ALL inversions on a completely (0-)simple
regular *-semigroup in terms of rho-cycles (Theorem E in 06-all-inversions.md).

Reuses the brute-force inversion finder from verify.py (which assumes no theory).
"""
import itertools, random
from math import gcd
from verify import (find_inversions, rees, rees0, sym_group, cyclic_group,
                    analyse_pair, perm_order, orbits_of)

def gmul(G, a, b):  return G[1][a][b]
def ginv(G, a):     return G[3][a]
def gone(G):        return G[2]

def star_condition(G, P):
    """P in normal form: p_ii = 1, p_ji = p_ij^{-1} (None = 0)."""
    n = len(P)
    for i in range(n):
        if P[i][i] != gone(G): return False
        for j in range(n):
            if (P[i][j] is None) != (P[j][i] is None): return False
            if P[i][j] is not None and P[j][i] != ginv(G, P[i][j]): return False
    return True

def p(G, P, i, j):
    return P[i][j]

def prod(G, *xs):
    out = gone(G)
    for x in xs:
        if x is None or out is None: return None
        out = gmul(G, out, x)
    return out

def star_cond_ast(G, P, rho):
    """(*): p_{rho k, rho^-1 j} = p_{rho k, k} p_{k j} p_{j, rho^-1 j}, all j,k."""
    n = len(P)
    rinv = [rho.index(x) for x in range(n)]
    if any(P[rho[i]][i] is None for i in range(n)): return False
    return all(P[rho[k]][rinv[j]] == prod(G, P[rho[k]][k], P[k][j], P[j][rinv[j]])
               for j in range(n) for k in range(n))

def cycles_flat(G, P, rho):
    for C in orbits_of(rho, range(len(P))):
        for i, j, l in itertools.product(C, repeat=3):
            if P[i][j] is None or P[j][l] is None: return False
            if prod(G, P[i][j], P[j][l]) != P[i][l]: return False
    return True

def hankel_condition(G, P, rho):
    """Given flat cycles: T_{u,v}(a,b) = p_{u,rho^a u} p_{rho^a u, rho^b v} p_{rho^b v, v}
    depends only on a+b, for all cycles C, C' with base points u, v."""
    cyc = orbits_of(rho, range(len(P)))
    for C in cyc:
        for C2 in cyc:
            u, v = C[0], C2[0]
            m, m2 = len(C), len(C2)
            T = {}
            for a in range(m):
                for b in range(m2):
                    t = prod(G, P[u][C[a]], P[C[a]][C2[b]], P[C2[b]][v])
                    key = (a + b) % gcd(m, m2)
                    if key in T and T[key] != t: return False
                    T[key] = t
    return True

def normalise(G, P, rho):
    """gauge c_i = p_{u i} (u = base point of the cycle of i); p'_{ij} = c_i p_ij c_j^{-1}."""
    n = len(P)
    c = [None] * n
    for C in orbits_of(rho, range(n)):
        for i in C: c[i] = P[C[0]][i]
    return [[prod(G, c[i], P[i][j], ginv(G, c[j])) for j in range(n)] for i in range(n)]

def phi_invariant(G, P, rho):
    """p_{rho i, j} = p_{i, rho j} for all i, j."""
    n = len(P)
    return all(P[rho[i]][j] == P[i][rho[j]] for i in range(n) for j in range(n))

def rho_of_inversion(mul, star, plus, nI, nG, zero):
    """read off rho from an inversion found by brute force (+-projection of R_i is in H_{i, rho i})."""
    idx = lambda i, g, j: (1 if zero else 0) + (i * nG + g) * nI + j
    rho = []
    for i in range(nI):
        found = [j for j in range(nI) for g in range(nG)
                 if mul[idx(i,g,j)][idx(i,g,j)] == idx(i,g,j) and plus[idx(i,g,j)] == idx(i,g,j)]
        assert len(found) == 1
        rho.append(found[0])
    return rho

def check_example(G, P, name, zero=False):
    assert star_condition(G, P)
    nI, nG = len(P), len(G[0])
    mul = rees0(G, range(nI), P) if zero else rees(G, range(nI), P)
    invs = find_inversions(mul)
    idx = lambda i, g, j: (1 if zero else 0) + (i * nG + g) * nI + j
    star = [0] * len(mul)
    for i, g, j in itertools.product(range(nI), range(nG), range(nI)):
        star[idx(i, g, j)] = idx(j, ginv(G, g), i)
    assert star in invs
    rhos_found = sorted(rho_of_inversion(mul, star, pl, nI, nG, zero) for pl in invs)
    rhos_pred = sorted(list(r) for r in itertools.permutations(range(nI)) if star_cond_ast(G, P, list(r)))
    assert rhos_found == rhos_pred, (rhos_found, rhos_pred)
    for rho in rhos_pred:
        assert cycles_flat(G, P, rho) and hankel_condition(G, P, rho)
        Pn = normalise(G, P, rho)
        assert star_condition(G, Pn) and phi_invariant(G, Pn, rho)
        for C in orbits_of(rho, range(nI)):
            assert all(Pn[i][j] == gone(G) for i in C for j in C)
        # closed under powers
        for e in range(1, perm_order(rho) + 1):
            r = list(range(nI))
            for _ in range(e): r = [rho[x] for x in r]
            assert r in rhos_pred
    # equivalence: (*)  <=>  flat cycles + Hankel, over all permutations
    for r in itertools.permutations(range(nI)):
        r = list(r)
        lhs = star_cond_ast(G, P, r)
        rhs = cycles_flat(G, P, r) and hankel_condition(G, P, r)
        assert lhs == rhs
    closed = all(([rho2[rho1[x]] for x in range(nI)] in rhos_pred) for rho1 in rhos_pred for rho2 in rhos_pred)
    print(f"{name}: |S|={len(mul)}, inversions={len(invs)}, admissible rho = {rhos_pred}, "
          f"closed under composition: {closed}")
    return invs, rhos_pred

def hankel_P(G, cycles, f):
    """Build P from cycle lengths and functions f[(C,C')] : Z/gcd -> G^0 (as lists), f[(C,C)] = 1."""
    pts = []
    for ci, m in enumerate(cycles):
        pts += [(ci, a) for a in range(m)]
    n = len(pts)
    P = [[None] * n for _ in range(n)]
    for x, (ci, a) in enumerate(pts):
        for y, (cj, b) in enumerate(pts):
            if ci == cj: P[x][y] = gone(G)
            else:
                g = gcd(cycles[ci], cycles[cj])
                P[x][y] = f[(ci, cj)][(a + b) % g]
    rho = [pts.index((ci, (a + 1) % cycles[ci])) for (ci, a) in pts]
    return P, rho

if __name__ == "__main__":
    Z3 = cyclic_group(3)
    S3 = sym_group(3)
    e3 = gone(Z3); t = 1
    # 1. the non-flat 4x4 example over Z3: two 2-cycles, f(0)=1, f(1)=t
    P = [[0, 0, 0, t],
         [0, 0, t, 0],
         [0, (-t) % 3, 0, 0],
         [(-t) % 3, 0, 0, 0]]
    check_example(Z3, P, "M[Z3;4,4;P] Hankel, two 2-cycles")
    # 2. random Hankel constructions over S3 / Z3, with zeros allowed, must all admit rho
    random.seed(1)
    for trial in range(6):
        G = S3 if trial % 2 else Z3
        cycles = random.choice([[2, 2], [3, 3], [2, 4], [1, 2, 2], [2, 3], [1, 3]])
        nG = len(G[0])
        f = {}
        for ci in range(len(cycles)):
            for cj in range(ci + 1, len(cycles)):
                g = gcd(cycles[ci], cycles[cj])
                vals = [random.choice([None] + list(range(nG))) for _ in range(g)]
                f[(ci, cj)] = vals
                f[(cj, ci)] = [None if v is None else ginv(G, v) for v in vals]
        P, rho = hankel_P(G, cycles, f)
        zero = any(v is None for row in P for v in row)
        invs, rhos = check_example(G, P, f"Hankel over {'S3' if G is S3 else 'Z3'}, cycles {cycles}, f={f}", zero=zero)
        assert rho in rhos
    # 3. all skew-symmetric P over Z3 with 3 rows, and the S3 flat example, re-checked against Theorem E
    for x, y, z in itertools.product(range(3), repeat=3):
        P = [[0, x, (-z) % 3], [(-x) % 3, 0, y], [z, (-y) % 3, 0]]
        check_example(Z3, P, f"M[Z3;3,3;P] (p01,p12,p20)=({x},{y},{z})")
