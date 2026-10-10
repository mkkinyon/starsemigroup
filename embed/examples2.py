import sys, time, itertools
sys.path.insert(0, '..')
from verify3 import group_over_band
from verify import find_inversions, is_semigroup
from embed import PnData, find_embedding, check_embedding
from enum_rss import is_rss

def test(name, mul, star, nmax, Ds):
    assert is_rss(mul, star)
    for n in range(1, nmax+1):
        t=time.time(); sols = find_embedding(mul, star, Ds[n])
        if sols:
            check_embedding(mul, star, sols[0], Ds[n]); print(f"{name}: |S|={len(mul)} embeds in P_{n} ({time.time()-t:.1f}s)", flush=True); return n
    print(f"{name}: |S|={len(mul)} NOT in P_n, n<={nmax}", flush=True)

def group_action_band(G, mulG, invG, A, act, with_identity=False):
    """S = G u (A x A) (u {1}); g(a,b) = (act(g,a), b); (a,b)g = (a, act(inv g, b)).
    G: list of group elements (indices), mulG table, invG list, act(g,a)."""
    elems = [('g', g) for g in G] + [('b', a, b) for a in A for b in A]
    if with_identity:
        elems.append(('1',))
    idx = {e: i for i, e in enumerate(elems)}
    n = len(elems)
    T = [[0]*n for _ in range(n)]
    for x in elems:
        for y in elems:
            if x[0] == '1': z = y
            elif y[0] == '1': z = x
            elif x[0] == 'g' and y[0] == 'g': z = ('g', mulG[x[1]][y[1]])
            elif x[0] == 'g': z = ('b', act(x[1], y[1]), y[2])
            elif y[0] == 'g': z = ('b', x[1], act(invG[y[1]], x[2]))
            else: z = ('b', x[1], y[2])
            T[idx[x]][idx[y]] = idx[z]
    star = []
    for x in elems:
        if x[0] == 'g': star.append(idx[('g', invG[x[1]])])
        elif x[0] == 'b': star.append(idx[('b', x[2], x[1])])
        else: star.append(idx[x])
    return T, star

if __name__ == "__main__":
    nmax = int(sys.argv[1]); Ds = {n: PnData(n) for n in range(1, nmax+1)}
    # S3 acting on {0,1,2}
    S3 = list(itertools.permutations(range(3)))
    comp = lambda p, q: tuple(p[q[i]] for i in range(3))   # (p q)(i) = p(q(i))
    mulG = [[S3.index(comp(p, q)) for q in S3] for p in S3]
    invG = [S3.index(tuple(sorted(range(3), key=lambda i: p[i]))) for p in S3]
    act = lambda g, a: S3[g][a]
    T, star = group_action_band(range(6), mulG, invG, range(3), act)
    test("S3 u (3x3 band)", T, star, nmax, Ds)
    A3 = [0, 3, 4] if False else None
    # Z3 = <(012)> acting on 3 points
    Z3 = [S3.index((0,1,2)), S3.index((1,2,0)), S3.index((2,0,1))]
    mulZ = [[Z3.index(mulG[g][h]) for h in Z3] for g in Z3]
    invZ = [Z3.index(invG[g]) for g in Z3]
    T, star = group_action_band(range(3), mulZ, invZ, range(3), lambda g, a: S3[Z3[g]][a])
    test("Z3 u (3x3 band) faithful", T, star, nmax, Ds)
    # Z3 acting trivially on 2x2 band, plus identity
    T, star = group_action_band(range(3), mulZ, invZ, range(2), lambda g, a: a, with_identity=True)
    test("{1} u Z3 u (2x2 band), trivial action", T, star, nmax, Ds)
    # Z2 acting trivially on 3x3 band
    T, star = group_action_band(range(2), [[0,1],[1,0]], [0,1], range(3), lambda g, a: a)
    test("Z2 u (3x3 band) trivial", T, star, nmax, Ds)
    # S3 acting on 2 points via sign
    sign = lambda g: 0 if sum(1 for i in range(3) for j in range(i) if S3[g][j] > S3[g][i]) % 2 == 0 else 1
    T, star = group_action_band(range(6), mulG, invG, range(2), lambda g, a: a ^ sign(g))
    test("S3 u (2x2 band) via sign", T, star, nmax, Ds)
