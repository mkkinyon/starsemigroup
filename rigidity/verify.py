"""
Computer verification for the notes on regular *-semigroups with two inversions.

Everything here works on a bare multiplication table, so the search for
inversions does NOT assume any of the structure theory; the structure theory is
then checked against the search results.
"""
import itertools
from math import lcm

# ---------------------------------------------------------------------------
# Generic tools for a finite semigroup given as a table mul[x][y]
# ---------------------------------------------------------------------------

def is_semigroup(mul):
    n = len(mul)
    return all(mul[mul[a][b]][c] == mul[a][mul[b][c]]
               for a in range(n) for b in range(n) for c in range(n))

def inverses(mul):
    n = len(mul)
    return [[y for y in range(n)
             if mul[mul[x][y]][x] == x and mul[mul[y][x]][y] == y]
            for x in range(n)]

def find_inversions(mul):
    """All maps d with d(d(x)) = x, d(xy) = d(y)d(x), x d(x) x = x.
    Backtracking with propagation (an anti-automorphism is determined by its
    values on a generating set)."""
    n = len(mul)
    V = inverses(mul)
    results = []

    def close(inv):
        inv = dict(inv)
        queue = list(inv.keys())
        while queue:
            x = queue.pop()
            for y in list(inv.keys()):
                for a, b in ((x, y), (y, x)):
                    c = mul[a][b]
                    d = mul[inv[b]][inv[a]]
                    for u, v in ((c, d), (d, c)):
                        if u in inv:
                            if inv[u] != v:
                                return None
                        else:
                            if v not in V[u]:
                                return None
                            inv[u] = v
                            queue.append(u)
        return inv

    def rec(inv):
        for x in range(n):
            if x not in inv:
                break
        else:
            results.append([inv[i] for i in range(n)])
            return
        for y in V[x]:
            if y in inv and inv[y] != x:
                continue
            new = dict(inv)
            new[x] = y
            new[y] = x
            new = close(new)
            if new is not None:
                rec(new)

    rec({})
    # independent re-check
    for d in results:
        assert all(d[d[x]] == x for x in range(n))
        assert all(d[mul[x][y]] == mul[d[y]][d[x]] for x in range(n) for y in range(n))
        assert all(mul[mul[x][d[x]]][x] == x for x in range(n))
    return results

def perm_order(p):
    n = len(p)
    seen = [False] * n
    k = 1
    for i in range(n):
        if not seen[i]:
            m, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                m += 1
            k = lcm(k, m)
    return k

def orbits_of(p, points):
    seen, orbs = set(), []
    for i in points:
        if i in seen:
            continue
        orb, j = [], i
        while j not in seen:
            seen.add(j)
            orb.append(j)
            j = p[j]
        orbs.append(orb)
    return orbs

# ---------------------------------------------------------------------------
# Analysis of a pair of inversions (star, plus) on a semigroup
# ---------------------------------------------------------------------------

def analyse_pair(mul, star, plus, verbose=True):
    n = len(mul)
    phi = [plus[star[x]] for x in range(n)]          # x -> x^{*+}
    k = perm_order(phi)
    Pstar = [e for e in range(n) if mul[e][e] == e and star[e] == e]
    # rho(e) = e^{+*} e^{+}  (the *-projection L-related to e^+)
    rho = {e: mul[star[plus[e]]][plus[e]] for e in Pstar}
    assert set(rho.values()) == set(Pstar), "rho is not a permutation of P*"
    orbs = orbits_of(rho, Pstar)
    lengths = sorted(len(o) for o in orbs)
    # Theorem part (2): k = order of rho
    assert k == lcm(*lengths), (k, lengths)
    bands = []
    for orb in orbs:
        m = len(orb)
        if m < 2:
            continue
        E = {(a, b): mul[orb[a]][orb[b]] for a in range(m) for b in range(m)}
        assert len(set(E.values())) == m * m
        # square band structure
        for (a, b), (c, d) in itertools.product(E, E):
            assert mul[E[a, b]][E[c, d]] == E[a, d]
        # closure under * and +, with the predicted formulas
        for (a, b), x in E.items():
            assert star[x] == E[b, a]
            assert plus[x] == E[(b - 1) % m, (a + 1) % m]
        # phi restricted to E has order exactly m
        restricted = {x: phi[x] for x in E.values()}
        o = 1
        while any(_iter(restricted, x, o) != x for x in E.values()):
            o += 1
        assert o == m
        bands.append((m, sorted(E.values())))
    # literal conjecture: a *,+-closed square band with |A| = k and distinct
    # restrictions <=> a rho-invariant union of orbits B, |B| = k, rho|B != id,
    # such that {e f : e,f in B} is a band.
    literal = False
    for r in range(1, len(orbs) + 1):
        for combo in itertools.combinations(orbs, r):
            B = [e for o in combo for e in o]
            if len(B) != k or all(len(o) == 1 for o in combo):
                continue
            E = {(a, b): mul[B[a]][B[b]] for a in range(k) for b in range(k)}
            ok = len(set(E.values())) == k * k and all(
                mul[E[a, b]][E[c, d]] == E[a, d]
                for (a, b), (c, d) in itertools.product(E, E))
            if ok:
                literal = True
    if verbose:
        print(f"  |S|={n}: k={k}, orbit lengths of rho on P* = {lengths}, "
              f"orbit bands of sizes {[m for m, _ in bands]}, "
              f"literal conjecture (|A|=k) holds: {literal}")
    return k, lengths, bands, literal

def _iter(f, x, o):
    for _ in range(o):
        x = f[x]
    return x

# ---------------------------------------------------------------------------
# Constructions
# ---------------------------------------------------------------------------

def square_band(n):
    idx = lambda a, b: a * n + b
    mul = [[0] * (n * n) for _ in range(n * n)]
    for a, b, c, d in itertools.product(range(n), repeat=4):
        mul[idx(a, b)][idx(c, d)] = idx(a, d)
    return mul

def sym_group(deg):
    elems = list(itertools.permutations(range(deg)))
    index = {g: i for i, g in enumerate(elems)}
    comp = lambda g, h: tuple(g[h[i]] for i in range(deg))   # (g h)(i) = g(h(i))
    table = [[index[comp(g, h)] for h in elems] for g in elems]
    e = index[tuple(range(deg))]
    inv = [index[tuple(sorted(range(deg), key=lambda i: g[i]))] for g in elems]
    return elems, table, e, inv

def cyclic_group(m):
    elems = list(range(m))
    table = [[(a + b) % m for b in elems] for a in elems]
    return elems, table, 0, [(-a) % m for a in elems]

def rees0(G, I, P):
    """M^0[G; I, I; P] with P[l][i] in G (index) or None (zero).
    Element 0 is the zero; (i,g,j) -> 1 + (i*|G| + g)*|I| + j."""
    elems, gt, e, ginv = G
    nG, nI = len(elems), len(I)
    idx = lambda i, g, j: 1 + (i * nG + g) * nI + j
    n = 1 + nI * nG * nI
    mul = [[0] * n for _ in range(n)]
    for i, g, j, k, h, l in itertools.product(range(nI), range(nG), range(nI),
                                              range(nI), range(nG), range(nI)):
        p = P[j][k]
        if p is not None:
            mul[idx(i, g, j)][idx(k, h, l)] = idx(i, gt[gt[g][p]][h], l)
    assert is_semigroup(mul)
    return mul

def rees(G, I, P):
    """completely simple M[G; I, I; P] (drop the zero)."""
    mul0 = rees0(G, I, P)
    return [[x - 1 for x in row[1:]] for row in mul0[1:]]

# ---------------------------------------------------------------------------
# Experiments
# ---------------------------------------------------------------------------

def run_all_pairs(mul, name):
    invs = find_inversions(mul)
    print(f"{name}: |S| = {len(mul)}, number of inversions = {len(invs)}")
    summary = set()
    for s, p in itertools.combinations(invs, 2):
        k, lengths, bands, literal = analyse_pair(mul, s, p, verbose=False)
        summary.add((k, tuple(lengths), literal))
    for k, lengths, literal in sorted(summary):
        print(f"   k={k}, orbit lengths {list(lengths)}, "
              f"literal conjecture holds: {literal}")
    return invs

if __name__ == "__main__":
    # 1. square bands: n! inversions
    for n in (2, 3, 4):
        run_all_pairs(square_band(n), f"square band {n}x{n}")

    # 2. the 5x5 counterexample: * = swap, + twisted by (12)(345)
    n = 5
    mul = square_band(n)
    beta = [1, 0, 4, 2, 3]          # x -> x beta : 0->1,1->0,2->4,3->2,4->3
    beta_inv = [beta.index(x) for x in range(n)]
    star = [b * n + a for a in range(n) for b in range(n)]               # (a,b)->(b,a)
    plus = [beta[b] * n + beta_inv[a] for a in range(n) for b in range(n)]  # (a,b)->(b beta, a beta^-1)
    print("Counterexample (5x5 band, beta=(12)(345)):")
    k, lengths, bands, literal = analyse_pair(mul, star, plus)
    assert k == 6 and not literal

    # 3. completely simple examples over S_3 with a 3-cycle rho, P flat/non-flat
    S3 = sym_group(3)
    elems, gt, e, ginv = S3
    a = elems.index((1, 0, 2))      # (0 1)
    b = elems.index((0, 2, 1))      # (1 2)
    c = ginv[gt[a][b]]              # c = (ab)^{-1}, so abc = 1
    P = [[e, a, ginv[c]],
         [ginv[a], e, b],
         [c, ginv[b], e]]
    mul = rees(S3, range(3), P)
    invs = run_all_pairs(mul, "M[S3;3,3;P], P flat (abc=1)")
    # non-flat P: replace c by something else
    c2 = a
    P2 = [[e, a, ginv[c2]],
          [ginv[a], e, b],
          [c2, ginv[b], e]]
    mul2 = rees(S3, range(3), P2)
    run_all_pairs(mul2, "M[S3;3,3;P'], P' not flat")

    # 4. a random-ish 0-simple example over Z_2 with 4 rows, block structure
    Z2 = cyclic_group(2)
    P4 = [[0, 1, None, None],
          [1, 0, None, None],
          [None, None, 0, 0],
          [None, None, 0, 0]]
    run_all_pairs(rees0(Z2, range(4), P4), "M^0[Z2;4,4;P] block diagonal")

    # 5. exhaustive: all skew-symmetric P over Z_3 with 3 rows (completely simple)
    Z3 = cyclic_group(3)
    seen = set()
    for x, y, z in itertools.product(range(3), repeat=3):
        P = [[0, x, (-z) % 3], [(-x) % 3, 0, y], [z, (-y) % 3, 0]]
        run_all_pairs(rees(Z3, range(3), P), f"M[Z3;3,3;P] with (p01,p12,p20)=({x},{y},{z})")

    # 6. 0-direct union of square bands of sizes 2, 3, 1 (block-diagonal P, trivial G)
    triv = cyclic_group(1)
    blocks = [[0, 1], [2, 3, 4], [5]]
    P6 = [[0 if any(i in b and j in b for b in blocks) else None for i in range(6)] for j in range(6)]
    run_all_pairs(rees0(triv, range(6), P6), "0-direct union of 2x2, 3x3, 1x1 bands")

    # 7. 5x5 band with an identity adjoined (two D-classes)
    n = 5
    b5 = square_band(n)
    N = n * n + 1
    mul = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if x == N - 1: mul[x][y] = y
            elif y == N - 1: mul[x][y] = x
            else: mul[x][y] = b5[x][y]
    assert is_semigroup(mul)
    run_all_pairs(mul, "(5x5 band)^1")

    # 8. genuine 0-direct union of a 2x2 band and a 3x3 band (14 elements)
    b2, b3 = square_band(2), square_band(3)
    N = 1 + 4 + 9
    mul = [[0] * N for _ in range(N)]
    for x in range(4):
        for y in range(4):
            mul[1 + x][1 + y] = 1 + b2[x][y]
    for x in range(9):
        for y in range(9):
            mul[5 + x][5 + y] = 5 + b3[x][y]
    assert is_semigroup(mul)
    run_all_pairs(mul, "0-direct union of 2x2 and 3x3 bands")
