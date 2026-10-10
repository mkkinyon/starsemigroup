"""Reduction search: can a proved condition be instantiated by terms (variables and theta_p(q)) over the
variables of a target condition so that its hypotheses hold on all instances and its conclusion is a|><|b?
Usage: python3 redsearch.py INSTFILE VARS [level]    e.g.  rp2inst4.pkl a,c,b,x1,x2,y
"""
import sys, pickle, random, itertools, time
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import mul
inst = pickle.load(open(sys.argv[1], 'rb')); V = sys.argv[2].split(','); n = max(max(max(b) for b in p) for p in inst[0]) + 1 if False else None
# determine n from the file name
n = int(''.join(ch for ch in sys.argv[1] if ch.isdigit())[-1])
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
# term pool
level = int(sys.argv[3]) if len(sys.argv) > 3 else 1
pool1 = list(V) + [(p, q) for p in V for q in V if p != q]          # (p,q) = theta_p(q)
pool = pool1 if level == 1 else pool1 + [(s, t) for s in pool1 for t in pool1 if s != t and not (isinstance(s, str) and isinstance(t, str))]
def val(t, I):
    if isinstance(t, str): return I[t]
    return th(val(t[0], I), val(t[1], I))
def fmt(t): return t if isinstance(t, str) else f"th_{fmt(t[0])}({fmt(t[1])})"
# proved conditions: (atoms, conclusion); atom kinds: mt, comm, eq(term,term) with terms being var or (var,var)
COND = {
 "(R')":  ([('mt','A','C'),('mt','C','B'),('comm','X','C'),('eq',('X','A'),('X','C')),('comm','Y','A'),('eq',('X','B'),('Y','B'))], ('A','B')),
 "(R)":   ([('mt','A','C'),('mt','C','B'),('comm','X','A'),('comm','X','C'),('eq',('X','B'),('X','C'))], ('A','B')),
 "(S)":   ([('mt','A','C'),('mt','C','B'),('mt','B','D'),('comm','C','D'),('eq',(('C','D'),'A'),(('C','D'),'B'))], ('A','D')),
 "(P1)":  ([('mt','A','C'),('mt','C','B'),('mt','B','D'),('comm','X','A'),('comm','X','D'),('eq',('X','C'),('X','B'))], ('A','D')),
 "(Q)":   ([('mt','A','C'),('mt','C','B'),('mt','B','D'),('comm','X','A'),('eq',('C','X'),('D','X')),('comm','Y','A'),('comm','Y','B'),('eq',('Y','C'),('Y','B'))], ('A','D')),
}
def evt(t, A, I):   # term over condition variables, A = assignment var -> pool term
    if isinstance(t, str): return val(A[t], I)
    return th(evt(t[0], A, I), evt(t[1], A, I))
def holds(at, A, I):
    if at[0] == 'mt':
        p, q = evt(at[1], A, I), evt(at[2], A, I); return th(p, q) == p and th(q, p) == q
    if at[0] == 'comm':
        p, q = evt(at[1], A, I), evt(at[2], A, I); return m(p, q) == m(q, p)
    return evt(at[1], A, I) == evt(at[2], A, I)
random.seed(0)
dist = [I for I in inst if len(set(I)) == len(V)]
S1 = [dict(zip(V, I)) for I in random.sample(dist, min(200, len(dist)))]
S2 = [dict(zip(V, I)) for I in random.sample(inst, min(3000, len(inst)))]
ALL = [dict(zip(V, I)) for I in inst]
def search(name, atoms, concl, ends):
    cv = []
    for at in atoms:
        for t in at[1:]:
            for v in (t if isinstance(t, tuple) else (t,)):
                for w in (v if isinstance(v, tuple) else (v,)):
                    if w not in cv: cv.append(w)
    found = []
    def allvars(t): return {t} if isinstance(t, str) else allvars(t[0]) | allvars(t[1])
    def rec(A, i, sample):
        if i == len(cv):
            found.append(dict(A)); return
        v = cv[i]
        choices = [V[0], V[2]] if v in concl else pool
        for t in choices:
            if v == concl[0] and t != ends[0]: continue
            if v == concl[1] and t != ends[1]: continue
            A[v] = t
            ready = [at for at in atoms if all(w in A for w in set().union(*(allvars(x) for x in at[1:]))) and any(v in allvars(x) for x in at[1:])]
            if all(holds(at, A, I) for at in ready for I in sample): rec(A, i + 1, sample)
            del A[v]
    import pickle, os
    ck = f'ck_{os.path.basename(sys.argv[1])}_{level}_{name}_{ends[0]}.pkl'
    if os.path.exists(ck): return pickle.load(open(ck, 'rb'))
    rec({}, 0, S1)
    out = []
    pathv = [v for v in cv if any(at[0] == 'mt' and v in at[1:] for at in atoms)]
    def nondeg(A):   # path terms pairwise distinct on most distinct instances
        cnt = sum(1 for I in S1 if len({evt(v, A, I) for v in pathv}) == len(pathv))
        return cnt >= 0.5 * len(S1)
    found = [A for A in found if nondeg(A)]
    for A in found:
        if all(holds(at, A, I) for at in atoms for I in S2) and all(holds(at, A, I) for at in atoms for I in ALL):
            out.append(A); print(f"  {name}: " + ', '.join(f"{v}={fmt(A[v])}" for v in cv), flush=True)
    pickle.dump(out, open(ck, 'wb'))
    return out
for name, (atoms, concl) in COND.items():
    for ends in ((V[0], V[2]), (V[2], V[0])):
        t0 = time.time(); r = search(name, atoms, concl, ends)
        print(f"{name} with ({concl[0]},{concl[1]})->({ends[0]},{ends[1]}): {len(r)} instantiations valid on all {len(ALL)} instances ({time.time()-t0:.0f}s)", flush=True)
