import sys, itertools, time
from embed import PnData, find_embedding, check_embedding

def strong_semilattice_band(Y, leq, A, f):
    """Y: list of indices; leq(a,b): a<=b in the semilattice; meet computed from leq;
    A[alpha]: list of labels; f[(alpha,beta)]: dict A[alpha]->A[beta] for alpha>=beta.
    Elements: (alpha, a, b). Involution: (alpha,a,b)* = (alpha,b,a)."""
    def meet(a, b):
        cands = [c for c in Y if leq(c, a) and leq(c, b)]
        return max(cands, key=lambda c: sum(leq(d, c) for d in Y))
    elems = [(al, a, b) for al in Y for a in A[al] for b in A[al]]
    idx = {e: i for i, e in enumerate(elems)}
    n = len(elems)
    T = [[0]*n for _ in range(n)]
    for (al, a, b) in elems:
        for (be, c, d) in elems:
            g = meet(al, be)
            fa = f[(al, g)][a] if al != g else a
            fd = f[(be, g)][d] if be != g else d
            T[idx[(al,a,b)]][idx[(be,c,d)]] = idx[(g, fa, fd)]
    star = [idx[(al, b, a)] for (al, a, b) in elems]
    return T, star, elems

if __name__ == "__main__":
    nmax = int(sys.argv[1])
    # chain alpha > beta, A_alpha={1,2} -> A_beta={1,2,3}
    Y = ['a', 'b']; leq = lambda x, y: x == y or (x == 'b' and y == 'a')
    A = {'a': [1, 2], 'b': [1, 2, 3]}; f = {('a', 'b'): {1: 1, 2: 2}}
    T, star, elems = strong_semilattice_band(Y, leq, A, f)
    from enum_rss import is_rss
    assert is_rss(T, star)
    print("|B| =", len(T))
    for n in range(1, nmax + 1):
        t = time.time(); D = PnData(n); sols = find_embedding(T, star, D)
        print(f"  P_{n}: {'embeds' if sols else 'no'} ({time.time()-t:.1f}s)", flush=True)
        if sols:
            check_embedding(T, star, sols[0], D)
            for e in elems:
                if e[1] == e[2]:
                    print("   ", e, sols[0][elems.index(e)])
            break
