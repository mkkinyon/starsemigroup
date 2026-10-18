#!/usr/bin/env python3
"""Hilbert-hotel search: violations of a projection-algebra quasi-identity in P(P_N).

Points: (i, j) with index i in [0, M) and fibre j in [0, f).  Each projection is a
partition with T/N marks whose blocks have index-span <= 1; for i >= d the structure is
1-periodic (pair and mark variables are shared with index d).  Every join class is
required to have index-span <= B, so a window of length M >= d + 2B + 3 reproduces the
infinite structure exactly, and hypotheses are enforced on the safe zone i <= M-1-B.

Conditions are given as lists of equations between terms  ('th', x, w) = theta_x(w)
and ('p', x) = x;  the conclusion a |><| b is required to FAIL.

Usage: hotel_sat.py COND f d B [solver]
"""
import sys, itertools, math
from pysat.solvers import Solver
from pysat.formula import CNF

def th(x, w): return ('th', x, w)
def pr(x): return ('p', x)
def matched(x, y): return [(th(x, y), pr(x)), (th(y, x), pr(y))]
def comm(x, y): return [(th(x, y), th(y, x))]

CONDS = {
  'Phi0':  dict(vars='abc', hyp=matched('a','c')+matched('c','b')+[(th('a','b'), pr('a'))]),
  'Psi0_2': dict(vars='pqr', hyp=[(th('p','q'), pr('q'))]+matched('q','r')+matched('r','p'), concl=('eq','q','p')),
  'A1':    dict(vars='abcx', hyp=matched('a','c')+matched('c','b')+comm('x','a')+comm('x','c')+[(th('x','b'), th('x','c'))]),
  'W2':    dict(vars='abcxy', hyp=matched('a','c')+matched('c','b')+comm('x','c')+comm('y','b')+comm('x','y')
                 +[(th('x','a'), th('x','c')), (th('y','a'), th('y','c'))]),
  'Hm':    dict(vars='abcyz', hyp=matched('a','c')+matched('c','b')+comm('y','c')
                 +[(th('y','b'), th('b','a')), (th('b','z'), pr('b')), (th('z','a'), th('z','b')), (th('y','z'), th('a','b'))]),
  'Hmp':   dict(vars='abcyz', hyp=matched('a','c')+matched('c','b')+comm('y','c')
                 +[(th('y','b'), th('b','a')), (th('b','z'), pr('b')), (th('a','z'), pr('a')), (th('y','z'), th('a','b'))]),
  'Ab':    dict(vars='abcyz', hyp=matched('a','c')+matched('c','b')+comm('y','c')
                 +[(th('a','y'), pr('a')), (th('z','b'), pr('b')), (th('z','y'), th('b','a')), (th('z','a'), th('a','b'))]),
  'X':     dict(vars='abct', hyp=[(th('b','c'), pr('b')), (th(th('a','t'),'b'), th('a','t')), (th(th('c','t'),'a'), th('c','t'))],
                 concl=('eq', th('a','t'), th('b','t'))),
}

class Enc:
    def __init__(s, f, d, B, M=None):
        s.f, s.d, s.B = f, d, B
        s.M = M or d + 2*B + 3
        s.pts = [(i, j) for i in range(s.M) for j in range(f)]
        s.safe = s.M - 1 - B
        s.nv = 0; s.cl = []; s.cache = {}
        s.FALSE = s.new(); s.cl.append([-s.FALSE])
        s.TRUE = -s.FALSE
    def new(s):
        s.nv += 1; return s.nv
    def canon(s, p, q=None):
        """shift a point or pair into the periodic template"""
        if q is None:
            i, j = p; return (min(i, s.d), j)
        (i, j), (k, l) = p, q
        if (i, j) > (k, l): (i, j), (k, l) = (k, l), (i, j)
        if i >= s.d:
            sh = i - s.d; return ((i - sh, j), (k - sh, l))
        return ((i, j), (k, l))
    def var(s, key):
        if key not in s.cache: s.cache[key] = s.new()
        return s.cache[key]
    # --- partition variables -------------------------------------------------
    def S(s, x, p, q):          # same block of projection x (span <= 1)
        if p == q: return s.TRUE
        if abs(p[0]-q[0]) > 1: return s.FALSE
        return s.var(('s', x) + s.canon(p, q))
    def T(s, x, p): return s.var(('t', x, s.canon(p)))
    def proj_axioms(s, x):
        for p in s.pts:
            for q in s.pts:
                if q == p or abs(p[0]-q[0]) > 1: continue
                if p < q:
                    s.cl.append([-s.S(x,p,q), -s.T(x,p), s.T(x,q)]); s.cl.append([-s.S(x,p,q), s.T(x,p), -s.T(x,q)])
                for r in s.pts:
                    if r in (p, q) or abs(q[0]-r[0]) > 1: continue
                    if abs(p[0]-r[0]) <= 1: s.cl.append([-s.S(x,p,q), -s.S(x,q,r), s.S(x,p,r)])
                    else: s.cl.append([-s.S(x,p,q), -s.S(x,q,r)])
    # --- joins ---------------------------------------------------------------
    def J(s, x, w, p, q):
        if p == q: return s.TRUE
        if abs(p[0]-q[0]) > s.B: return s.FALSE
        key = ('J', x, w) + tuple(sorted((p, q)))
        if key in s.cache: return s.cache[key]
        s.build_join(x, w); return s.cache[key]
    def build_join(s, x, w):
        if ('built', x, w) in s.cache: return
        s.cache[('built', x, w)] = True
        pairs = [(p, q) for p in s.pts for q in s.pts if p < q and abs(p[0]-q[0]) <= s.B]
        level = {}
        for (p, q) in pairs:
            v = s.new(); level[(p, q)] = v
            e1, e2 = s.S(x,p,q), s.S(w,p,q)
            s.cl.append([-v, e1, e2]); s.cl.append([-e1, v]); s.cl.append([-e2, v])
        L = math.ceil(math.log2((s.B+1)*s.f)) + 1
        nbr = {p: [q for q in s.pts if q != p and abs(p[0]-q[0]) <= s.B] for p in s.pts}
        for _ in range(L):
            nxt = {}
            def cur(p, q):
                if p == q: return s.TRUE
                return level[(min(p,q), max(p,q))]
            for (p, r) in pairs:
                v = s.new(); nxt[(p, r)] = v
                ms = []
                s.cl.append([-cur(p, r), v])
                for q in nbr[p]:
                    if q == r or abs(q[0]-r[0]) > s.B: continue
                    m = s.new(); ms.append(m)
                    s.cl.append([-m, cur(p,q)]); s.cl.append([-m, cur(q,r)]); s.cl.append([-cur(p,q), -cur(q,r), m])
                    s.cl.append([-m, v])
                s.cl.append([-v, cur(p, r)] + ms)
            # no class of span > B: forbid two-step connections with span > B
            for p in s.pts:
                for q in nbr[p]:
                    for r in nbr[q]:
                        if r == p or abs(p[0]-r[0]) <= s.B: continue
                        if p < r: s.cl.append([-cur(p,q), -cur(q,r)])
            level = nxt
        for (p, q), v in level.items(): s.cache[('J', x, w) + (p, q)] = v
    # --- theta values ----------------------------------------------------------
    def blk(s, term, p, q):
        """literal: p, q in the same block of term (p != q, span <= B)"""
        if term[0] == 'p': return s.S(term[1], p, q)
        x, w = term[1], term[2]
        if isinstance(x, tuple) or isinstance(w, tuple):
            raise ValueError('nested terms need materialisation; not supported here')
        key = ('blk', term, p, q)
        if key in s.cache: return s.cache[key]
        v = s.new(); s.cache[key] = v
        tp, tq, j, e = s.T(x,p), s.T(x,q), s.J(x,w,p,q), s.S(x,p,q)
        # v <-> (tp & tq & j) | (~tp & ~tq & e)
        a1, a2 = s.new(), s.new()
        s.cl += [[-a1, tp], [-a1, tq], [-a1, j], [-tp, -tq, -j, a1]]
        s.cl += [[-a2, -tp], [-a2, -tq], [-a2, e], [tp, tq, -e, a2]]
        s.cl += [[-v, a1, a2], [-a1, v], [-a2, v]]
        return v
    def tmark(s, term, p):
        if term[0] == 'p': return s.T(term[1], p)
        x, w = term[1], term[2]
        key = ('tm', term, p)
        if key in s.cache: return s.cache[key]
        v = s.new(); s.cache[key] = v
        ms = []
        for q in s.pts:
            if abs(p[0]-q[0]) > s.B: continue
            m = s.new(); ms.append(m)
            jq = s.J(x,w,p,q)
            s.cl += [[-m, s.T(w,q)], [-m, jq], [-s.T(w,q), -jq, m]]
        # v <-> T(x,p) & OR ms
        s.cl.append([-v, s.T(x,p)])
        s.cl.append([-v] + ms)
        for m in ms: s.cl.append([-s.T(x,p), -m, v])
        return v
    def safe_pairs(s):
        return [(p, q) for p in s.pts for q in s.pts if p < q and abs(p[0]-q[0]) <= s.B and p[0] <= s.safe and q[0] <= s.safe]
    def safe_pts(s): return [p for p in s.pts if p[0] <= s.safe]
    def equal(s, t1, t2):
        for (p, q) in s.safe_pairs():
            a, b = s.blk(t1,p,q), s.blk(t2,p,q); s.cl += [[-a, b], [-b, a]]
        for p in s.safe_pts():
            a, b = s.tmark(t1,p), s.tmark(t2,p); s.cl += [[-a, b], [-b, a]]
    def differ_lits(s, t1, t2):
        lits = []
        for (p, q) in s.safe_pairs():
            a, b = s.blk(t1,p,q), s.blk(t2,p,q); x = s.new(); lits.append(x)
            s.cl += [[-x, a, b], [-x, -a, -b]]
        for p in s.safe_pts():
            a, b = s.tmark(t1,p), s.tmark(t2,p); x = s.new(); lits.append(x)
            s.cl += [[-x, a, b], [-x, -a, -b]]
        return lits

def run(name, f, d, B, solver='cadical153'):
    C = CONDS[name]; e = Enc(f, d, B)
    for x in C['vars']: e.proj_axioms(x)
    for (t1, t2) in C['hyp']:
        if any(isinstance(t[1], tuple) or isinstance(t[2], tuple) for t in (t1, t2) if t[0]=='th'):
            print('nested term in', name); return
        e.equal(t1, t2)
    concl = C.get('concl', ('mt', 'a', 'b'))
    if concl[0] == 'mt':
        a, b = concl[1], concl[2]
        lits = e.differ_lits(th(a,b), pr(a)) + e.differ_lits(th(b,a), pr(b))
    else:
        t1 = pr(concl[1]) if isinstance(concl[1], str) else concl[1]
        t2 = pr(concl[2]) if isinstance(concl[2], str) else concl[2]
        lits = e.differ_lits(t1, t2)
    e.cl.append(lits)
    print(f'{name}: f={f} d={d} B={B} M={e.M}  vars={e.nv} clauses={len(e.cl)}', flush=True)
    with Solver(name=solver, bootstrap_with=e.cl) as S:
        ok = S.solve()
        print('SAT' if ok else 'UNSAT', flush=True)
        if ok:
            model = set(l for l in S.get_model() if l > 0)
            for x in C['vars']:
                # print blocks of x on the window
                par = {p: p for p in e.pts}
                def find(p):
                    while par[p] != p: p = par[p]
                    return p
                for p in e.pts:
                    for q in e.pts:
                        if p < q and abs(p[0]-q[0]) <= 1 and e.S(x,p,q) in model: par[find(p)] = find(q)
                blocks = {}
                for p in e.pts: blocks.setdefault(find(p), []).append(p)
                desc = []
                for bl in sorted(blocks.values()):
                    mark = 'T' if e.T(x, bl[0]) in model else 'N'
                    if mark == 'N' and len(bl) == 1: continue
                    desc.append(mark + '{' + ','.join(f'{i}.{j}' for (i,j) in bl) + '}')
                print(f'  {x}: ' + ' '.join(desc) + '   (N-singletons omitted)')
            verify(e, model, C)
    return ok

# ---------------------------------------------------------------------------
# Independent verification of a model: extend the window periodically to length
# MM and compute theta-values by brute-force partition multiplication; compare
# on the interior (index <= MM-1-margin).
def extract(e, model, x):
    par = {p: p for p in e.pts}
    def find(p):
        while par[p] != p: p = par[p]
        return p
    for p in e.pts:
        for q in e.pts:
            if p < q and abs(p[0]-q[0]) <= 1 and e.S(x,p,q) in model: par[find(p)] = find(q)
    blocks = {}
    for p in e.pts: blocks.setdefault(find(p), []).append(p)
    return [(sorted(bl), e.T(x, bl[0]) in model) for bl in blocks.values()]

def extend(e, blocks, MM):
    """periodic extension: blocks touching index >= d are translated by all shifts"""
    out = set()
    for bl, t in blocks:
        lo = min(i for (i, j) in bl)
        if lo <= e.d:
            out.add((tuple(bl), t))
        elif lo == e.d + 1:   # generic template blocks (their left pairs are periodic)
            for sh in range(0, MM):
                nb = tuple((i+sh, j) for (i, j) in bl)
                if max(i for (i, j) in nb) < MM: out.add((nb, t))
    # points not covered become N-singletons
    cov = set(p for bl, t in out for p in bl)
    for i in range(MM):
        for j in range(e.f):
            if (i, j) not in cov: out.add((((i, j),), False))
    return out

def to_partition(blocks):
    P = []
    for bl, t in blocks:
        if t: P.append(frozenset((p, s) for p in bl for s in (0, 1)))
        else:
            P.append(frozenset((p, 0) for p in bl)); P.append(frozenset((p, 1) for p in bl))
    return frozenset(P)

def mult(Pa, Pb, pts):
    par = {}
    def f(x):
        while par.setdefault(x, x) != x: x = par[x]
        return x
    def u(p, q): par[f(p)] = f(q)
    for bl in Pa:
        l = [('u', p) if s == 0 else ('m', p) for (p, s) in bl]
        for q in l[1:]: u(l[0], q)
    for bl in Pb:
        l = [('m', p) if s == 0 else ('l', p) for (p, s) in bl]
        for q in l[1:]: u(l[0], q)
    cls = {}
    for p in pts:
        cls.setdefault(f(('u', p)), set()).add((p, 0)); cls.setdefault(f(('l', p)), set()).add((p, 1))
    return frozenset(frozenset(v) for v in cls.values())

def verify(e, model, C, MM=24, margin=4):
    pts = [(i, j) for i in range(MM) for j in range(e.f)]
    P = {x: to_partition(extend(e, extract(e, model, x), MM)) for x in C['vars']}
    def ev(t):
        if t[0] == 'p': return P[t[1]]
        w = P[t[2]] if isinstance(t[2], str) else ev(t[2])
        return mult(mult(P[t[1]], w, pts), P[t[1]], pts)
    def interior(bl): return all(p[0] <= MM-1-margin for (p, s) in bl)
    def same(A, B): return not [bl for bl in A ^ B if interior(bl)]
    ok = True
    for (t1, t2) in C['hyp']:
        if not same(ev(t1), ev(t2)): print('  VERIFY FAIL hypothesis', t1, t2); ok = False
    concl = C.get('concl', ('mt', 'a', 'b'))
    if concl[0] == 'mt':
        a, b = concl[1], concl[2]
        fails = (not same(ev(th(a,b)), P[a])) or (not same(ev(th(b,a)), P[b]))
    else:
        t1 = pr(concl[1]) if isinstance(concl[1], str) else concl[1]
        t2 = pr(concl[2]) if isinstance(concl[2], str) else concl[2]
        fails = not same(ev(t1), ev(t2))
    if not fails: print('  VERIFY FAIL: conclusion holds'); ok = False
    print('  verification on window', MM, ':', 'OK' if ok else 'FAILED')
    return ok

if __name__ == '__main__':
    name, f, d, B = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    solver = sys.argv[5] if len(sys.argv) > 5 else 'cadical153'
    run(name, f, d, B, solver)

