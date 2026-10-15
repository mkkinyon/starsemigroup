"""Substitution reduction for K4: can a proved condition be instantiated by terms over a,b,c,y,z so that its hypotheses
hold on all K4 instances of P(P_4) and its conclusion is a|><|b?   Usage: python3 k4red.py [level]"""
import sys, time, random, itertools, pickle, os
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
def le(p, q): return theta(q, p) == p
level = int(sys.argv[1]) if len(sys.argv) > 1 else 1
n = 4; P = projections(n); random.seed(1)
if os.path.exists('k4inst4.pkl'): INST = pickle.load(open('k4inst4.pkl', 'rb'))
else:
    INST = []
    for a in P:
        for c in P:
            if not matched(a, c): continue
            Ys = [y for y in P if theta(a, y) == a and commute(y, c)]
            if not Ys: continue
            for b in P:
                if not matched(b, c): continue
                u = theta(a, b); v = theta(b, a)
                for z in P:
                    if not (le(b, z) and theta(z, a) == u): continue
                    for y in Ys:
                        if theta(z, y) == v: INST.append({'a': a, 'b': b, 'c': c, 'y': y, 'z': z})
    pickle.dump(INST, open('k4inst4.pkl', 'wb'))
print(len(INST), 'instances')
V = ['a', 'b', 'c', 'y', 'z']
pool1 = list(V) + [(p, q) for p in V for q in V if p != q]      # (p,q) = theta_p(q)
pool = pool1 if level == 1 else pool1 + [(s, t) for s in pool1 for t in pool1 if s != t and not (isinstance(s, str) and isinstance(t, str))]
memo = {}
def val(t, I):
    if isinstance(t, str): return I[t]
    k = (t, id(I))
    if k not in memo: memo[k] = theta(val(t[0], I), val(t[1], I))
    return memo[k]
def fmt(t): return t if isinstance(t, str) else 'th_%s(%s)' % (fmt(t[0]), fmt(t[1]))
COND = {
 "(R)":   ([('mt','A','C'),('mt','C','B'),('comm','X','A'),('comm','X','C'),('eq',('X','B'),('X','C'))], ('A','B')),
 "(R')":  ([('mt','A','C'),('mt','C','B'),('comm','X','C'),('eq',('X','A'),('X','C')),('comm','Y','A'),('eq',('X','B'),('Y','B'))], ('A','B')),
 "(W2)":  ([('mt','A','C'),('mt','C','B'),('comm','X','C'),('comm','Y','B'),('comm','X','Y'),('eq',('X','A'),('X','C')),('eq',('Y','A'),('Y','C'))], ('A','B')),
 "(S)":   ([('mt','A','C'),('mt','C','B'),('mt','B','D'),('comm','C','D'),('eq',(('C','D'),'A'),(('C','D'),'B'))], ('A','D')),
 "(P1)":  ([('mt','A','C'),('mt','C','B'),('mt','B','D'),('comm','X','A'),('comm','X','D'),('eq',('X','C'),('X','B'))], ('A','D')),
 "(Q)":   ([('mt','A','C'),('mt','C','B'),('mt','B','D'),('comm','X','A'),('eq',('C','X'),('D','X')),('comm','Y','A'),('comm','Y','B'),('eq',('Y','C'),('Y','B'))], ('A','D')),
}
def evt(t, A, I):
    if isinstance(t, str): return val(A[t], I)
    return theta(evt(t[0], A, I), evt(t[1], A, I))
def holds(at, A, I):
    if at[0] == 'mt': p, q = evt(at[1], A, I), evt(at[2], A, I); return theta(p, q) == p and theta(q, p) == q
    if at[0] == 'comm': return commute(evt(at[1], A, I), evt(at[2], A, I))
    return evt(at[1], A, I) == evt(at[2], A, I)
S1 = random.sample(INST, 150); S2 = random.sample(INST, 2000)
def allvars(t): return {t} if isinstance(t, str) else allvars(t[0]) | allvars(t[1])
for name, (atoms, concl) in COND.items():
    cv = []
    for at in atoms:
        for t in at[1:]:
            for w in allvars(t):
                if w not in cv: cv.append(w)
    for ends in (('a', 'b'), ('b', 'a')):
        t0 = time.time(); found = []
        def rec(A, i):
            if i == len(cv): found.append(dict(A)); return
            v = cv[i]
            choices = [ends[0]] if v == concl[0] else [ends[1]] if v == concl[1] else pool
            for t in choices:
                A[v] = t
                ready = [at for at in atoms if all(w in A for w in set().union(*(allvars(x) for x in at[1:]))) and any(v in allvars(x) for x in at[1:])]
                if all(holds(at, A, I) for at in ready for I in S1): rec(A, i + 1)
                del A[v]
        rec({}, 0)
        pathv = [v for v in cv if any(at[0] == 'mt' and v in at[1:] for at in atoms)]
        def nondeg(A):
            cnt = sum(1 for I in S1 if len({evt(v, A, I) for v in pathv}) == len(pathv))
            return cnt >= 0.5 * len(S1)
        found = [A for A in found if nondeg(A)]
        out = [A for A in found if all(holds(at, A, I) for at in atoms for I in S2) and all(holds(at, A, I) for at in atoms for I in INST)]
        print('%s (%s,%s): %d candidates after sample, %d valid on all instances (%.0fs)' % (name, ends[0], ends[1], len(found), len(out), time.time() - t0), flush=True)
        for A in out[:10]: print('    ' + ', '.join('%s=%s' % (v, fmt(A[v])) for v in cv))
