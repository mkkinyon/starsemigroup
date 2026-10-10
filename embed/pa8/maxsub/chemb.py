"""Explicit embeddings of the maximal subalgebras of P^ch_n into P(P_m).
Points: al, be, ga and p_l, q_l (l = 1..n, the pair X_l).  A projection is given by its list of blocks with a T/N flag;
bottom elements are rank 0.  'merged' X_l means {p_l,q_l} is one N-block, 'sep' means two singleton blocks."""
import sys, json
sys.path.insert(0, '/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/embed/pa8/wn')
from pmon import mul
from family import build

def make(n, omit):
    L = [l for l in range(1, n + 1) if l != omit]            # the X-pairs present
    pts = ['al', 'be', 'ga'] + [f'p{l}' for l in L] + [f'q{l}' for l in L]
    def X(merged):   # merged: set of l with {p_l,q_l} one block; others separate
        out = []
        for l in L:
            if l in merged: out.append(({f'p{l}', f'q{l}'}, 'N'))
            else: out += [({f'p{l}'}, 'N'), ({f'q{l}'}, 'N')]
        return out
    allL = set(L)
    def Xge(j): return {l for l in L if l > j}      # merged for l > j  (e_j)
    E = {}
    if omit in ('x', 'b'):        # omit x_i (omit = i handled below) or omit b: R'-part of all e_j and N(x_k) is {al be}{ga} ... see notes
        pass
    if isinstance(omit, int):     # omit x_i
        i = omit
        Rpart = lambda left: [({'al', 'be'}, 'N'), ({'ga'}, 'N')] if left else [({'al'}, 'N'), ({'be'}, 'N'), ({'ga'}, 'N')]
        E['a'] = [({'al'}, 'T'), ({'be', 'ga'}, 'N')] + X(allL)
        E['c'] = [({'al', 'be'}, 'T'), ({'ga'}, 'N')] + X(allL)
        E['b'] = [({'be'}, 'T'), ({'al'}, 'N'), ({'ga'}, 'N')] + X(set())
        for k in L:
            E[f'x{k}'] = [({f'p{k}'}, 'T'), ({f'q{k}'}, 'T')] + Rpart(k < i) + X({l for l in L if l > k}) [0:0] + [bl for bl in X({l for l in L if l > k}) if f'p{k}' not in bl[0] and f'q{k}' not in bl[0]]
        E['d'] = [({'al'}, 'N'), ({'be', 'ga'}, 'N')] + X(allL)
        for j in range(0, n + 1):
            E[f'e{j}'] = Rpart(j <= i - 1) + X(Xge(j))
    elif omit == 'b':
        R = [({'al', 'be'}, 'N'), ({'ga'}, 'N')]
        E['a'] = [({'al'}, 'T'), ({'be', 'ga'}, 'N')] + X(allL)
        E['c'] = [({'al', 'be'}, 'T'), ({'ga'}, 'N')] + X(allL)
        for k in L:
            E[f'x{k}'] = [({f'p{k}'}, 'T'), ({f'q{k}'}, 'T')] + R + [bl for bl in X({l for l in L if l > k}) if f'p{k}' not in bl[0] and f'q{k}' not in bl[0]]
        E['d'] = [({'al'}, 'N'), ({'be', 'ga'}, 'N')] + X(allL)
        for j in range(0, n + 1): E[f'e{j}'] = R + X(Xge(j))
    elif omit == 'c':
        R = [({'al'}, 'N'), ({'be'}, 'N'), ({'ga'}, 'N')]
        E['a'] = [({'al'}, 'T'), ({'be', 'ga'}, 'N')] + X(allL)
        E['b'] = [({'be'}, 'T'), ({'al'}, 'N'), ({'ga'}, 'N')] + X(set())
        for k in L:
            E[f'x{k}'] = [({f'p{k}'}, 'T'), ({f'q{k}'}, 'T')] + R + [bl for bl in X({l for l in L if l > k}) if f'p{k}' not in bl[0] and f'q{k}' not in bl[0]]
        E['d'] = [({'al'}, 'N'), ({'be', 'ga'}, 'N')] + X(allL)
        for j in range(0, n + 1): E[f'e{j}'] = R + X(Xge(j))
    elif omit == 'a':
        R = [({'al'}, 'N'), ({'be'}, 'N'), ({'ga'}, 'N')]
        E['c'] = [({'al'}, 'T'), ({'be'}, 'T'), ({'ga'}, 'N')] + X(allL)
        E['b'] = [({'al'}, 'T'), ({'be'}, 'T'), ({'ga'}, 'N')] + X(set())
        for k in L:
            E[f'x{k}'] = [({f'p{k}'}, 'T'), ({f'q{k}'}, 'T')] + R + [bl for bl in X({l for l in L if l > k}) if f'p{k}' not in bl[0] and f'q{k}' not in bl[0]]
        E['d'] = [({'al'}, 'N'), ({'be', 'ga'}, 'N')] + X(allL)
        for j in range(0, n + 1): E[f'e{j}'] = R + X(Xge(j))
    return pts, E

def to_partition(blocks, pts, m):
    """pmon representation: a partition of {0..m-1} u {m..2m-1} (lower copy = +m); T-block B -> B u (B+m)."""
    idx = {p: i for i, p in enumerate(pts)}
    out = []
    for B, kind in blocks:
        top = [idx[p] for p in B]
        if kind == 'T': out.append(tuple(sorted(top + [t + m for t in top])))
        else: out.append(tuple(sorted(top))); out.append(tuple(sorted(t + m for t in top)))
    return tuple(sorted(out))

def check(n, omit):
    T, names = build(n); N = len(T)
    name_omit = f'x{omit}' if isinstance(omit, int) else omit
    S = [i for i in range(N) if names[i] != name_omit]
    pts, E = make(n, omit); m = len(pts)
    assert set(E) == {names[i] for i in S}, (set(E) ^ {names[i] for i in S})
    # sanity: each E[.] is a partition of pts
    for nm_, bl in E.items():
        cover = [p for B, _ in bl for p in B]
        assert sorted(cover) == sorted(pts), (nm_, sorted(cover))
    P = {nm_: to_partition(bl, pts, m) for nm_, bl in E.items()}
    assert len(set(P.values())) == len(P), "not injective"
    bad = 0
    for i in S:
        for j in S:
            x, y = names[i], names[j]
            prod = mul(mul(P[y], P[x], m), P[y], m)          # theta_y(x) = y x y  ... check convention below
            want = names[T[i][j]]
            if prod != P[want]: bad += 1
    return m, bad

if __name__ == '__main__':
    import pickle
    sys.path.insert(0, '/home/claude/pa8w/embed/pa8/rpp')
    # convention check: in pmon, mul(p,q,n) = p*q (p on top). theta_y(x) = y x y.  T[i][j] = i*j = theta_j(i).
    for n in range(1, int(sys.argv[1]) + 1):
        for omit in ['a', 'c', 'b'] + list(range(1, n + 1)):
            m, bad = check(n, omit)
            print(f"n={n} omit {omit}: m={m}, {bad} wrong products", flush=True)
