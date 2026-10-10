"""Explicit embeddings of the maximal subalgebras of P^{R'}_n (rpfam.py) into P(P_m).  Bottom elements are rank 0.
Points: al, be, ga, de, dp (delta'), ze (zeta) and the pairs p_l, q_l (l < n).  See notes, Section 5.18."""
import sys
sys.path.insert(0, '/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/embed/pa8/impl/rp2'); sys.path.insert(0, '/home/claude/pa8w/embed/pa8/maxsub')
from pmon import mul
from rpfam import build
from chemb import to_partition
N_ = lambda *bs: [(set(b.split()), 'N') for b in bs]
T_ = lambda *bs: [(set(b.split()), 'T') for b in bs]

def make(n, omit):
    L = [l for l in range(1, n) if l != omit]
    def X(merged):
        out = []
        for l in L:
            if l in merged: out.append(({f'p{l}', f'q{l}'}, 'N'))
            else: out += [({f'p{l}'}, 'N'), ({f'q{l}'}, 'N')]
        return out
    def Xk(l, merged):   # N-part of x_l on the other pairs
        return [bl for bl in X(merged) if f'p{l}' not in bl[0] and f'q{l}' not in bl[0]]
    pairs = set(L); sep = set()
    gt = lambda j: {l for l in L if l > j}
    PQ = [({f'p{l}'}, 'T') for l in L] + [({f'q{l}'}, 'T') for l in L]
    E = {}
    if isinstance(omit, int):                      # omit x_i, 1 <= i <= n-1
        i = omit; pts = ['al', 'be', 'ga', 'de', 'dp', 'ze']
        R = lambda left: N_('al be', 'ga', 'ze') + (N_('de dp') if left else N_('de', 'dp'))
        E['a'] = T_('al be') + N_('ga', 'de ze', 'dp') + X(pairs)
        E['c'] = T_('al be') + N_('ga', 'de dp', 'ze') + X(pairs)
        E['b'] = T_('de') + N_('al', 'be dp', 'ga', 'ze') + X(sep)
        for l in L: E[f'x{l}'] = T_(f'p{l}', f'q{l}') + R(l < i) + Xk(l, gt(l))
        E[f'x{n}'] = T_('de') + N_('al be', 'ga', 'dp', 'ze') + X(sep)
        E['k'] = T_('de', 'dp', 'ze') + PQ + N_('al be', 'ga')
        E['d'] = N_('al be', 'ga', 'de ze', 'dp') + X(pairs)
        for j in range(n): E[f'e{j}'] = R(j < i) + X(gt(j))
        E[f'e{n}'] = N_('al', 'be dp', 'ga', 'ze', 'de') + X(sep)
    elif omit == 'a':
        pts = ['al', 'be', 'ga', 'de', 'ze']
        R = N_('al be', 'ga', 'de', 'ze')
        E['c'] = T_('al be') + N_('ga', 'de', 'ze') + X(pairs)
        E['b'] = T_('be de') + N_('al', 'ga', 'ze') + X(sep)
        for l in L: E[f'x{l}'] = T_(f'p{l}', f'q{l}') + R + Xk(l, gt(l))
        E[f'x{n}'] = T_('de') + N_('al be', 'ga', 'ze') + X(sep)
        E['k'] = T_('de', 'ze') + PQ + N_('al be', 'ga')
        E['d'] = N_('al be', 'ga', 'de ze') + X(pairs)
        for j in range(n): E[f'e{j}'] = R + X(gt(j))
        E[f'e{n}'] = N_('al', 'ga', 'ze', 'be de') + X(sep)
    elif omit == 'b':
        pts = ['al', 'be', 'ga', 'de', 'ze']
        R = N_('al be', 'ga', 'de', 'ze')
        E['a'] = T_('al be') + N_('ga', 'de ze') + X(pairs)
        E['c'] = T_('al be') + N_('ga', 'de', 'ze') + X(pairs)
        for l in L: E[f'x{l}'] = T_(f'p{l}', f'q{l}') + R + Xk(l, gt(l))
        E[f'x{n}'] = T_('de') + N_('al be', 'ga', 'ze') + X(sep)
        E['k'] = T_('de', 'ze') + PQ + N_('al be', 'ga')
        E['d'] = N_('al be', 'ga', 'de ze') + X(pairs)
        for j in range(n): E[f'e{j}'] = R + X(gt(j))
        E[f'e{n}'] = N_('al', 'be', 'ga', 'de', 'ze') + X(sep)
    elif omit == 'c':
        pts = ['al', 'be', 'ga', 'de', 'ze']
        R = N_('al', 'be', 'ga', 'de', 'ze')
        E['a'] = T_('al') + N_('be', 'ga', 'de ze') + X(pairs)
        E['b'] = T_('be de') + N_('al', 'ga', 'ze') + X(sep)
        for l in L: E[f'x{l}'] = T_(f'p{l}', f'q{l}') + R + Xk(l, gt(l))
        E[f'x{n}'] = T_('de') + N_('al', 'be', 'ga', 'ze') + X(sep)
        E['k'] = T_('de', 'ze') + PQ + N_('al', 'be', 'ga')
        E['d'] = N_('al', 'be', 'ga', 'de ze') + X(pairs)
        for j in range(n): E[f'e{j}'] = R + X(gt(j))
        E[f'e{n}'] = N_('al', 'ga', 'ze', 'be de') + X(sep)
    elif omit == 'k':
        pts = ['al', 'be', 'ga', 'de']
        R = N_('al be', 'ga', 'de')
        E['a'] = T_('al') + N_('be ga', 'de') + X(pairs)
        E['c'] = T_('al be') + N_('ga', 'de') + X(pairs)
        E['b'] = T_('be de') + N_('al', 'ga') + X(sep)
        for l in L: E[f'x{l}'] = T_(f'p{l}', f'q{l}') + R + Xk(l, gt(l))
        E[f'x{n}'] = T_('de') + N_('al be', 'ga') + X(sep)
        E['d'] = N_('al', 'be ga', 'de') + X(pairs)
        for j in range(n): E[f'e{j}'] = R + X(gt(j))
        E[f'e{n}'] = N_('al', 'ga', 'be de') + X(sep)
    pts = pts + [f'p{l}' for l in L] + [f'q{l}' for l in L]
    return pts, E

def check(n, omit):
    T, names = build(n); N = len(T)
    name_omit = f'x{omit}' if isinstance(omit, int) else omit
    S = [i for i in range(N) if names[i] != name_omit]
    pts, E = make(n, omit); m = len(pts)
    assert set(E) == {names[i] for i in S}, (set(E) ^ {names[i] for i in S})
    for nm_, bl in E.items():
        cover = [p for B, _ in bl for p in B]
        assert sorted(cover) == sorted(pts), (nm_, sorted(cover), sorted(pts))
    P = {nm_: to_partition(bl, pts, m) for nm_, bl in E.items()}
    assert len(set(P.values())) == len(P), "not injective"
    bad = []
    for i in S:
        for j in S:
            x, y = names[i], names[j]
            prod = mul(mul(P[y], P[x], m), P[y], m)
            if prod != P[names[T[i][j]]]: bad.append((x, y, names[T[i][j]]))
    return m, bad

if __name__ == '__main__':
    for n in range(1, int(sys.argv[1]) + 1):
        for omit in ['a', 'c', 'b', 'k'] + list(range(1, n)):
            m, bad = check(n, omit)
            print(f"n={n} omit {omit}: m={m}, {len(bad)} wrong products {bad[:4]}", flush=True)
