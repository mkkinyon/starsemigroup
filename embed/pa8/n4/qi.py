"""Generic quasi-identities over projection algebras: atoms
  ('mt', p, q)              p ~ q
  ('le', p, q)              p <= q           (theta_q(p) = p)
  ('comm', p, q)            theta_p(q) = theta_q(p)
  ('eq', (p, q), (r, s))    theta_p(q) = theta_r(s)        [a term (p, q) means theta_p(q); a bare variable name means itself]
  ('fix', p, q)             theta_p(q) = p   (half matching: p q p = p)
Variables are strings.  valid(atoms, concl, m): full SAT validity in P(P_m) (variables not assumed distinct).
violated_in(T, atoms, concl): an assignment in the finite algebra T (T[x][y] = theta_y(x)) satisfying the atoms and
failing the conclusion, or None."""
import sys, os, itertools
os.environ.setdefault('EMBED_DIR', '/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/embed')
from pa_sat import solve

def _terms_of(atoms, concl):
    V = []
    def addv(v):
        if v not in V: V.append(v)
    for at in list(atoms) + [concl]:
        for x in at[1:]:
            if isinstance(x, tuple):
                for y in x: addv(y)
            else: addv(x)
    return V

def table(atoms, concl=None):
    """partial table (None = unknown) over the variables plus fresh elements for the theta-terms in 'eq' atoms"""
    V = _terms_of(atoms, concl if concl else ('le', atoms[0][1] if not isinstance(atoms[0][1], tuple) else atoms[0][1][0], atoms[0][1] if not isinstance(atoms[0][1], tuple) else atoms[0][1][0]))
    idx = {v: i for i, v in enumerate(V)}; k = len(V)
    cons = {}
    def set_(p, q, v):      # theta_p(q) = v  <=>  T[q][p] = v
        key = (idx[q], idx[p])
        if key in cons and cons[key] != v: raise ValueError('conflict')
        cons[key] = v
    parent = {}
    def find(t):
        parent.setdefault(t, t)
        while parent[t] != t: parent[t] = parent[parent[t]]; t = parent[t]
        return t
    eqs = []
    for at in atoms:
        if at[0] == 'mt': set_(at[1], at[2], idx[at[1]]); set_(at[2], at[1], idx[at[2]])
        elif at[0] == 'le': set_(at[2], at[1], idx[at[1]])
        elif at[0] == 'fix': set_(at[1], at[2], idx[at[1]])
        elif at[0] == 'comm': eqs.append(((at[1], at[2]), (at[2], at[1])))
        elif at[0] == 'eq': eqs.append((at[1], at[2]))
    for t1, t2 in eqs:
        a, b = find(t1), find(t2)
        if a != b: parent[a] = b
    classes = {}
    for t in list(parent): classes.setdefault(find(t), []).append(t)
    fresh = k
    for cl in classes.values():
        named = {cons[(idx[t[1]], idx[t[0]])] for t in cl if isinstance(t, tuple) and (idx[t[1]], idx[t[0]]) in cons}
        named |= {idx[t] for t in cl if not isinstance(t, tuple)}
        if len(named) > 1: raise ValueError('equality of named elements')
        v = named.pop() if named else fresh
        if v == fresh: fresh += 1
        for t in cl:
            if isinstance(t, tuple): set_(t[0], t[1], v)
    T = [[None] * fresh for _ in range(fresh)]
    for i in range(fresh): T[i][i] = i
    for (x, y), v in cons.items(): T[x][y] = v
    return T, idx

def valid(atoms, concl, m, verbose=False):
    T, idx = table(atoms, concl); N = len(T)
    negs = []
    if concl[0] == 'mt':
        negs = [((concl[2], concl[1]), idx[concl[1]]), ((concl[1], concl[2]), idx[concl[2]])]   # theta_p(q) != p
    elif concl[0] == 'le': negs = [((concl[1], concl[2]), idx[concl[1]])]
    elif concl[0] == 'fix': negs = [((concl[2], concl[1]), idx[concl[1]])]
    elif concl[0] in ('eq', 'comm'):
        t1, t2 = (concl[1], concl[2]) if concl[0] == 'eq' else ((concl[1], concl[2]), (concl[2], concl[1]))
        T2 = [row[:] + [None, None] for row in T] + [[None] * (N + 2) for _ in range(2)]
        for i in range(N + 2): T2[i][i] = i
        els = []
        for k, t in enumerate((t1, t2)):
            if isinstance(t, tuple):
                w = T2[idx[t[1]]][idx[t[0]]]
                if w is None: w = N + k; T2[idx[t[1]]][idx[t[0]]] = w
            else: w = idx[t]
            els.append(w)
        if els[0] == els[1]: return True
        return solve(T2, m, distinct=[tuple(els)], verbose=verbose, symbreak=False) is None
    for (q, p), v in negs:        # T[q][p] = theta_p(q) should differ from v
        T2 = [row[:] + [None] for row in T] + [[None] * (N + 1)]
        for i in range(N + 1): T2[i][i] = i
        w = T2[idx[q]][idx[p]]
        if w is not None:
            if w == v: continue
            if solve(T, m, distinct=[(w, v)], verbose=verbose, symbreak=False) is not None: return False
            continue
        T2[idx[q]][idx[p]] = N
        if solve(T2, m, distinct=[(N, v)], verbose=verbose, symbreak=False) is not None: return False
    return True

def violated_in(T, atoms, concl):
    N = len(T); th = lambda p, q: T[q][p]
    V = _terms_of(atoms, concl)
    def ev(t, A): return th(A[t[0]], A[t[1]]) if isinstance(t, tuple) else A[t]
    for vals in itertools.product(range(N), repeat=len(V)):
        A = dict(zip(V, vals)); ok = True
        for at in atoms:
            k = at[0]
            if k == 'mt': ok = th(A[at[1]], A[at[2]]) == A[at[1]] and th(A[at[2]], A[at[1]]) == A[at[2]]
            elif k == 'le': ok = th(A[at[2]], A[at[1]]) == A[at[1]]
            elif k == 'fix': ok = th(A[at[1]], A[at[2]]) == A[at[1]]
            elif k == 'comm': ok = th(A[at[1]], A[at[2]]) == th(A[at[2]], A[at[1]])
            elif k == 'eq': ok = ev(at[1], A) == ev(at[2], A)
            if not ok: break
        if not ok: continue
        c = concl
        if c[0] == 'mt': fails = not (th(A[c[1]], A[c[2]]) == A[c[1]] and th(A[c[2]], A[c[1]]) == A[c[2]])
        elif c[0] == 'le': fails = th(A[c[2]], A[c[1]]) != A[c[1]]
        elif c[0] == 'fix': fails = th(A[c[1]], A[c[2]]) != A[c[1]]
        if fails: return A
    return None
