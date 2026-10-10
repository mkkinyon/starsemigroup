"""
Verification for the global structure theorem (07-global-structure.md):

  every inversion has the form  x^+ = rho^{-1}(x*x) x* rho(xx*)  for a unique
  permutation rho of P*, and a permutation rho gives an inversion iff
  phi_rho(x) = rho^{-1}(xx*) x rho(x*x) is an automorphism of S.

Also: Lemma H (reduction of multiplicativity to special pairs), the H u (AxA)
family (inversions <-> centraliser of H in Sym(A)), and that rho need not
preserve the projection algebra.
"""
import itertools
from verify import (find_inversions, square_band, is_semigroup, rees0, rees,
                    cyclic_group, sym_group, perm_order)
from verify2 import hankel_P

def green(mul):
    n = len(mul)
    R = [frozenset([x] + mul[x]) for x in range(n)]          # x S^1
    L = [frozenset([x] + [mul[y][x] for y in range(n)]) for x in range(n)]
    Rrel = lambda a, b: R[a] == R[b]
    Lrel = lambda a, b: L[a] == L[b]
    # D = J for finite: use two-sided ideal
    J = [frozenset({x} | set(mul[x]) | {mul[y][x] for y in range(n)} |
                   {mul[mul[y][x]][z] for y in range(n) for z in range(n)}) for x in range(n)]
    Drel = lambda a, b: J[a] == J[b]
    return Rrel, Lrel, Drel

def phi_from_rho(mul, star, rho):
    n = len(mul)
    rinv = {v: k for k, v in rho.items()}
    return [mul[mul[rinv[mul[x][star[x]]]][x]][rho[mul[star[x]][x]]] for x in range(n)]

def plus_from_rho(mul, star, rho):
    phi = phi_from_rho(mul, star, rho)
    return [phi[star[x]] for x in range(len(mul))]

def is_automorphism(mul, f):
    n = len(mul)
    return len(set(f)) == n and all(f[mul[a][b]] == mul[f[a]][f[b]] for a in range(n) for b in range(n))

def is_inversion(mul, d):
    n = len(mul)
    return (all(d[d[x]] == x for x in range(n)) and
            all(d[mul[x][y]] == mul[d[y]][d[x]] for x in range(n) for y in range(n)) and
            all(mul[mul[x][d[x]]][x] == x for x in range(n)))

def check_global(mul, star, name, all_perms=True):
    n = len(mul)
    Pstar = [e for e in range(n) if mul[e][e] == e and star[e] == e]
    invs = find_inversions(mul)
    assert star in invs
    # (1) every inversion is the rho-twist of * for rho(e) = e^{+*} e^{+}
    rhos = []
    for plus in invs:
        rho = {e: mul[star[plus[e]]][plus[e]] for e in Pstar}
        assert sorted(rho.values()) == sorted(Pstar)
        assert plus_from_rho(mul, star, rho) == plus
        assert is_automorphism(mul, phi_from_rho(mul, star, rho))
        rhos.append(rho)
    assert len({tuple(sorted(r.items())) for r in rhos}) == len(invs)   # injective
    # (2) converse over all permutations of P*, and Lemma H
    if all_perms:
        Rrel, Lrel, Drel = green(mul)
        special = [(a, b) for a in range(n) for b in range(n)
                   if Rrel(mul[a][b], a) or Lrel(mul[a][b], b) or (a in Pstar and b in Pstar)]
        count = 0
        for perm in itertools.permutations(Pstar):
            rho = dict(zip(Pstar, perm))
            phi = phi_from_rho(mul, star, rho)
            aut = is_automorphism(mul, phi)
            inv = is_inversion(mul, plus_from_rho(mul, star, rho))
            assert aut == inv
            # Lemma H: bijective + multiplicative on special pairs  <=> automorphism
            lemmaH = len(set(phi)) == n and all(phi[mul[a][b]] == mul[phi[a]][phi[b]] for a, b in special)
            assert lemmaH == aut
            count += aut
        assert count == len(invs)
    print(f"{name}: |S|={n}, |P*|={len(Pstar)}, inversions={len(invs)}"
          + (f" (= admissible permutations of P* out of {len(Pstar)}!)" if all_perms else ""))
    return invs, rhos

def group_over_band(H, A):
    """S = H u (A x A): h(a,b) = (h a, b), (a,b)h = (a, h^{-1} b), (a,b)(c,d) = (a,d).
    H is a list of permutations of A (tuples), closed under composition."""
    nA = len(A)
    hidx = {h: i for i, h in enumerate(H)}
    comp = lambda g, h: tuple(g[h[i]] for i in range(nA))
    hinv = lambda h: tuple(sorted(range(nA), key=lambda i: h[i]))
    nH = len(H)
    n = nH + nA * nA
    band = lambda a, b: nH + a * nA + b
    mul = [[0] * n for _ in range(n)]
    for i, g in enumerate(H):
        for j, h in enumerate(H):
            mul[i][j] = hidx[comp(g, h)]
        for a in range(nA):
            for b in range(nA):
                mul[i][band(a, b)] = band(g[a], b)
                mul[band(a, b)][i] = band(a, hinv(g)[b])
    for a, b, c, d in itertools.product(range(nA), repeat=4):
        mul[band(a, b)][band(c, d)] = band(a, d)
    assert is_semigroup(mul)
    star = [hidx[hinv(h)] for h in H] + [band(b, a) for a in range(nA) for b in range(nA)]
    return mul, star

if __name__ == "__main__":
    # A. square bands, (5x5 band)^1-type, 0-direct unions
    for m in (2, 3):
        mul = square_band(m)
        star = [b * m + a for a in range(m) for b in range(m)]
        check_global(mul, star, f"square band {m}x{m}")
    b2, b3 = square_band(2), square_band(3)
    N = 1 + 4 + 9
    mul = [[0] * N for _ in range(N)]
    for x in range(4):
        for y in range(4): mul[1 + x][1 + y] = 1 + b2[x][y]
    for x in range(9):
        for y in range(9): mul[5 + x][5 + y] = 5 + b3[x][y]
    star = [0] + [1 + (b * 2 + a) for a in range(2) for b in range(2)] + [5 + (b * 3 + a) for a in range(3) for b in range(3)]
    check_global(mul, star, "0-direct union of 2x2 and 3x3 bands")

    # B. H u (A x A) with A = {0,1,2}: inversions <-> centraliser of H in Sym(A)
    A = range(3)
    S3 = list(itertools.permutations(A))
    for Hname, H in [("trivial", [(0, 1, 2)]),
                     ("<(01)>", [(0, 1, 2), (1, 0, 2)]),
                     ("<(012)>", [(0, 1, 2), (1, 2, 0), (2, 0, 1)]),
                     ("S3", S3)]:
        mul, star = group_over_band(H, A)
        invs, rhos = check_global(mul, star, f"H u (3x3 band), H = {Hname}")
        cent = [g for g in S3 if all(tuple(g[h[i]] for i in A) == tuple(h[g[i]] for i in A) for h in H)]
        assert len(invs) == len(cent), (len(invs), len(cent))
        print(f"    centraliser of H in Sym(3) has order {len(cent)} -- matches")

    # C. Rees examples with nontrivial groups (all permutations of P* still feasible: |P*| <= 6)
    Z3 = cyclic_group(3)
    P = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]]
    mul = rees(Z3, range(4), P)
    nI, nG = 4, 3
    idx = lambda i, g, j: (i * nG + g) * nI + j
    star = [0] * len(mul)
    for i, g, j in itertools.product(range(nI), range(nG), range(nI)):
        star[idx(i, g, j)] = idx(j, (-g) % 3, i)
    check_global(mul, star, "M[Z3;4,4;P] Hankel (not orthodox)")

    # D. rho need not be an automorphism of the projection algebra (e -> f e f)
    f = {(0, 1): [None, 1, None], (1, 0): [None, 2, None]}
    P, rho_pts = hankel_P(Z3, [3, 3], f)
    mul = rees0(Z3, range(6), P)
    nI, nG = 6, 3
    idx0 = lambda i, g, j: 1 + (i * nG + g) * nI + j
    star = [0] * len(mul)
    for i, g, j in itertools.product(range(nI), range(nG), range(nI)):
        star[idx0(i, g, j)] = idx0(j, (-g) % 3, i)
    invs, rhos = check_global(mul, star, "M^0[Z3;6,6;P] two 3-cycles, f=(0,t,0)", all_perms=False)
    Pstar = sorted(rhos[0].keys())
    bad = 0
    for rho in rhos:
        if any(rho[mul[mul[f_][e]][f_]] != mul[mul[rho[f_]][rho[e]]][rho[f_]] for e in Pstar for f_ in Pstar):
            bad += 1
    print(f"    of its {len(rhos)} admissible rho, {bad} are NOT automorphisms of the projection algebra (P*, e -> fef)")
    assert bad > 0
