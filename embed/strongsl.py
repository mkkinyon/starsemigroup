"""Strong semilattices of completely simple regular *-semigroups (normal form Rees matrices)."""
import sys, time, itertools
sys.path.insert(0, '..')
from embed import PnData, find_embedding, check_embedding
from enum_rss import is_rss

def rees_elems(G, I):
    return [(i, g, j) for i in I for g in range(len(G)) for j in I]

def strong_semilattice(Y, leq, comps, maps):
    """comps[alpha] = (Gmul, Ginv, I, P) with P[i][j] in G (normal form); maps[(alpha,beta)] = function on elements."""
    def meet(a, b):
        c = [x for x in Y if leq(x, a) and leq(x, b)]
        return max(c, key=lambda x: sum(leq(d, x) for d in Y))
    elems = [(al,) + e for al in Y for e in rees_elems(comps[al][0], comps[al][2])]
    idx = {e: k for k, e in enumerate(elems)}
    def mulc(al, x, y):
        Gmul, Ginv, I, P = comps[al]
        (i, g, j), (k, h, l) = x, y
        return (i, Gmul[Gmul[g][P[j][k]]][h], l)
    def mp(al, be, x):
        return x if al == be else maps[(al, be)](x)
    n = len(elems)
    T = [[0]*n for _ in range(n)]
    for x in elems:
        for y in elems:
            g = meet(x[0], y[0])
            T[idx[x]][idx[y]] = idx[(g,) + mulc(g, mp(x[0], g, x[1:]), mp(y[0], g, y[1:]))]
    star = []
    for x in elems:
        al, (i, g, j) = x[0], x[1:]
        star.append(idx[(al, j, comps[al][1][g], i)])
    return T, star, elems

def test(name, T, star, nmax, Ds):
    assert is_rss(T, star)
    for n in range(1, nmax + 1):
        t = time.time(); sols = find_embedding(T, star, Ds[n])
        if sols:
            check_embedding(T, star, sols[0], Ds[n]); print(f"{name}: |S|={len(T)} embeds in P_{n} ({time.time()-t:.1f}s)", flush=True); return n
    print(f"{name}: |S|={len(T)} NOT in P_n, n<={nmax}", flush=True)

if __name__ == "__main__":
    nmax = int(sys.argv[1]); Ds = {n: PnData(n) for n in range(1, nmax + 1)}
    Z2 = ([[0,1],[1,0]], [0,1]); Z1 = ([[0]], [0])
    Y = ['a', '0']; leq = lambda x, y: x == y or x == '0'
    # 1) Z2 x (2x2) -> 2x2 band (kill group)
    comps = {'a': (Z2[0], Z2[1], [0,1], [[0,0],[0,0]]), '0': (Z1[0], Z1[1], [0,1], [[0,0],[0,0]])}
    maps = {('a','0'): lambda x: (x[0], 0, x[2])}
    T, star, _ = strong_semilattice(Y, leq, comps, maps); test("Z2x(2x2) -> 2x2 band", T, star, nmax, Ds)
    # 2) Z2 x (2x2) -> M[Z2;3,3;nonflat] injective on projections, identity on group
    P3 = [[0,1,0],[1,0,0],[0,0,0]]
    comps = {'a': (Z2[0], Z2[1], [0,1], [[0,0],[0,0]]), '0': (Z2[0], Z2[1], [0,1,2], P3)}
    maps = {('a','0'): lambda x: (x[0], x[1], x[2])}
    # check hom: (i,g,j)(k,h,l) = (i, g p_jk h, l) in top (p=1) vs bottom p_jk for j,k in {0,1}: p01 = 1 (=t) -> not a hom! use rows {0,2}
    maps = {('a','0'): lambda x: ({0:0,1:2}[x[0]], x[1], {0:0,1:2}[x[2]])}
    T, star, _ = strong_semilattice(Y, leq, comps, maps); test("Z2x(2x2) -> M[Z2;3,3;nonflat] rows {0,2}", T, star, nmax, Ds)
    # 3) 2x2 band -> M[Z2;3,3;nonflat] (rows 0,2), group trivial on top
    comps = {'a': (Z1[0], Z1[1], [0,1], [[0,0],[0,0]]), '0': (Z2[0], Z2[1], [0,1,2], P3)}
    maps = {('a','0'): lambda x: ({0:0,1:2}[x[0]], 0, {0:0,1:2}[x[2]])}
    T, star, _ = strong_semilattice(Y, leq, comps, maps); test("2x2 band -> M[Z2;3,3;nonflat]", T, star, nmax, Ds)
    # 4) M[Z2;2,2;p01=t] (nonflat? 2 rows always flat) -> M[Z2;3,3;nonflat] rows {0,1}: top P = [[0,1],[1,0]]
    comps = {'a': (Z2[0], Z2[1], [0,1], [[0,1],[1,0]]), '0': (Z2[0], Z2[1], [0,1,2], P3)}
    maps = {('a','0'): lambda x: (x[0], x[1], x[2])}
    T, star, _ = strong_semilattice(Y, leq, comps, maps); test("M[Z2;2,2;t] -> M[Z2;3,3;nonflat] rows {0,1}", T, star, nmax, Ds)
    # 5) three levels: Z2 (group) -> Z2 x (2x2) -> 2x2 band
    Y = ['b', 'a', '0']; leq = lambda x, y: x == y or x == '0' or (x == 'a' and y == 'b')
    comps = {'b': (Z2[0], Z2[1], [0], [[0]]), 'a': (Z2[0], Z2[1], [0,1], [[0,0],[0,0]]), '0': (Z1[0], Z1[1], [0,1], [[0,0],[0,0]])}
    maps = {('b','a'): lambda x: (0, x[1], 0), ('a','0'): lambda x: (x[0], 0, x[2]), ('b','0'): lambda x: (0, 0, 0)}
    T, star, _ = strong_semilattice(Y, leq, comps, maps); test("Z2 -> Z2x(2x2) -> 2x2", T, star, nmax, Ds)
