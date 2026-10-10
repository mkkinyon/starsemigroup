"""Extract a quasi-identity from a non-embeddable projection algebra C (table C[x][y] = theta_y(x)).
Hypotheses: a subset H of the atoms  theta_y(x) = v  (x != y) of the diagram of C.  Conclusion: an atom that fails in C:
  ('mt', p, q)   p ~ q          (theta_p(q) = p  and  theta_q(p) = q)
  ('le', p, q)   p <= q         (theta_q(p) = p)
  ('eq', (x, y), (z, w))        theta_y(x) = theta_w(z)      (terms may also be plain variables: ('var', v))
H => concl is valid in P(P_m) iff  H & not concl  is unsatisfiable, tested by SAT with a partial table (pa_sat.solve
with None entries; the negation is encoded by new elements for the terms and a 'distinct' pair).
Greedy minimisation: drop atoms one at a time while validity at level m is kept.  Usage: see main."""
import sys, os, json, itertools, time
EMBED = os.environ.get("EMBED_DIR", "/mnt/user-data/outputs/starsemigroup/embed"); sys.path.insert(0, EMBED)
from pa_sat import solve

def build(k, H, terms):
    """partial table over k elements plus one new element per term; returns table and the indices of the terms"""
    n = k + len(terms); T = [[None] * n for _ in range(n)]
    for i in range(n): T[i][i] = i
    for (x, y), v in H.items(): T[x][y] = v
    idx = []
    for j, t in enumerate(terms):
        if t[0] == 'var': idx.append(t[1])
        else:
            x, y = t[1]; T[x][y] = k + j; idx.append(k + j)   # theta_y(x) = new element
    return T, idx

def negations(k, H, concl):
    """list of (table, distinct-pairs) whose joint unsatisfiability means H => concl"""
    kind = concl[0]
    if kind == 'mt':
        p, q = concl[1], concl[2]
        return negations(k, H, ('fix', p, q)) + negations(k, H, ('fix', q, p))
    if kind == 'fix':      # ('fix', p, q): theta_p(q) = p
        p, q = concl[1], concl[2]
        T, idx = build(k, H, [('th', (q, p))]); return [(T, [(idx[0], p)])]
    if kind == 'le':       # p <= q: theta_q(p) = p
        p, q = concl[1], concl[2]
        T, idx = build(k, H, [('th', (p, q))]); return [(T, [(idx[0], p)])]
    if kind == 'eq':
        t1 = ('th', concl[1]) if isinstance(concl[1], tuple) and len(concl[1]) == 2 and not isinstance(concl[1][0], str) else concl[1]
        t2 = ('th', concl[2]) if isinstance(concl[2], tuple) and len(concl[2]) == 2 and not isinstance(concl[2][0], str) else concl[2]
        T, idx = build(k, H, [t1, t2]); return [(T, [(idx[0], idx[1])])]
    raise ValueError(concl)

def valid(k, H, concl, m, verbose=False):
    for T, dpairs in negations(k, H, concl):
        if solve(T, m, distinct=dpairs, verbose=verbose, symbreak=False) is not None: return False
    return True

def fails_in(C, H, concl):
    """does the quasi-identity H => concl fail in C under the identity assignment?  (H holds by construction)"""
    th = lambda p, q: C[q][p]
    kind = concl[0]
    if kind == 'mt': return not (th(concl[1], concl[2]) == concl[1] and th(concl[2], concl[1]) == concl[2])
    if kind == 'fix': return th(concl[1], concl[2]) != concl[1]
    if kind == 'le': return th(concl[2], concl[1]) != concl[1]
    if kind == 'eq':
        ev = lambda t: C[t[0]][t[1]] if not (isinstance(t[0], str)) else t[1]
        return ev(concl[1]) != ev(concl[2])

def minimise(C, concl, m, order=None, verbose=True):
    k = len(C)
    H = {(x, y): C[x][y] for x in range(k) for y in range(k) if x != y}
    assert fails_in(C, H, concl)
    assert valid(k, H, concl, m), "full diagram does not imply the conclusion (C embeds?)"
    if order is None:      # generic products first, then order atoms x <= y, then 'fixing' atoms theta_y(x) = y
        pri = lambda a: 0 if H[a] not in a else (1 if H[a] == a[0] else 2)
        order = sorted(H, key=lambda a: (pri(a), a))
    atoms = order
    for a in atoms:
        H2 = dict(H); del H2[a]
        t = time.time(); ok = valid(k, H2, concl, m)
        if ok: H = H2
        if verbose: print(f"  drop th_{a[1]}({a[0]})={C[a[0]][a[1]]}: {'ok' if ok else 'needed'} ({time.time()-t:.1f}s), {len(H)} atoms left", flush=True)
    return H

def fmt(H, concl):
    s = ", ".join(f"th_{y}({x})={v}" for (x, y), v in sorted(H.items()))
    return s + "  =>  " + str(concl)

if __name__ == "__main__":
    C = json.loads(sys.argv[1]); concl = json.loads(sys.argv[2]); m = int(sys.argv[3])
    concl = tuple(tuple(c) if isinstance(c, list) else c for c in concl)
    H = minimise(C, concl, m)
    print(fmt(H, concl))
    print(json.dumps({"H": [[list(a), v] for a, v in H.items()], "concl": concl}))
