"""Checks for 08-rigid.md: the 5-element band, closure of rigidity under products
(empirical), and genericity of rigidity for 3-row Rees matrix semigroups."""
import itertools
from verify import find_inversions, is_semigroup, inverses, rees, cyclic_group

def T5():
    """S = {s} u (2x2 band), s(a,b) = (0,b), (a,b)s = (a,0)."""
    band = lambda a, b: 1 + 2 * a + b
    mul = [[0] * 5 for _ in range(5)]
    for a in range(2):
        for b in range(2):
            mul[0][band(a, b)] = band(0, b)
            mul[band(a, b)][0] = band(a, 0)
            for c in range(2):
                for d in range(2):
                    mul[band(a, b)][band(c, d)] = band(a, d)
    assert is_semigroup(mul)
    return mul

def product(m1, m2):
    n1, n2 = len(m1), len(m2)
    idx = lambda x, y: x * n2 + y
    mul = [[0] * (n1 * n2) for _ in range(n1 * n2)]
    for x, y, u, v in itertools.product(range(n1), range(n2), range(n1), range(n2)):
        mul[idx(x, y)][idx(u, v)] = idx(m1[x][u], m2[y][v])
    return mul

if __name__ == "__main__":
    T = T5()
    invs = find_inversions(T)
    assert len(invs) == 1 and all(len(V) == 4 for V in inverses(T)[1:])
    print("5-element band T: unique inversion; every band element has 4 inverses")

    Z2 = cyclic_group(2)
    M = rees(Z2, range(3), [[0, 1, 0], [1, 0, 0], [0, 0, 0]])   # p01 = t, not flat
    assert len(find_inversions(M)) == 1
    for name, S in [("T x T", product(T, T)), ("T x M", product(T, M)), ("M x M", product(M, M))]:
        k = len(find_inversions(S))
        print(f"{name}: |S| = {len(S)}, inversions = {k}")
        assert k == 1

    for q in (2, 3, 5, 7):
        tot = rig = 0
        for x, y, z in itertools.product(range(q), repeat=3):
            tot += 1
            rig += (x + y + z) % q != 0          # 3 rows: rigid iff P not flat
        print(f"3 rows over Z_{q}: rigid fraction {rig}/{tot} = {rig/tot:.3f} = 1 - 1/{q}")
