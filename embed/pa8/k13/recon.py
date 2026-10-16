"""Reconnaissance of a 2-path condition with auxiliaries in P(P_n): instances, dropped-hypothesis map for a><b,
consequence atoms (depth-1 terms) on the full instances, and dropped-hypothesis map of each consequence atom.
Usage: python3 recon.py COND n [cap]      (COND in K1a K1b K1c K3a K3b K3c; cap = max instances per enumeration)
Conditions (notes, Section 5.13); u = theta_a(b), v = theta_b(a); th(p,q) = theta_p(q)."""
import sys, time, itertools, pickle
import numpy as np
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
th = lambda p, q: ('th', p, q)
COND = {
 'K1a': [('aya=a', th('a','y'), 'a'), ('th_y(b)=th_z(x)', th('y','b'), th('z','x')), ('th_x(b)=u', th('x','b'), 'u'),
         ('u=v', 'u', 'v'), ('th_c(z)=th_x(z)', th('c','z'), th('x','z'))],
 'K1b': [('aya=a', th('a','y'), 'a'), ('th_z(c)=b', th('z','c'), 'b'), ('th_y(a)=th_y(x)', th('y','a'), th('y','x')),
         ('th_x(c)=u', th('x','c'), 'u'), ('th_z(x)=u', th('z','x'), 'u'), ('th_y(z)=v', th('y','z'), 'v')],
 'K1c': [('bxb=b', th('b','x'), 'b'), ('th_y(a)=th_z(y)', th('y','a'), th('z','y')), ('th_c(z)=th_x(a)', th('c','z'), th('x','a')),
         ('th_x(a)=th_y(x)', th('x','a'), th('y','x')), ('th_z(x)=v', th('z','x'), 'v')],
 'K3a': [('th_z(c)=a', th('z','c'), 'a'), ('byb=b', th('b','y'), 'b'), ('th_x(c)=th_x(y)', th('x','c'), th('x','y')),
         ('th_y(b)=th_y(x)', th('y','b'), th('y','x')), ('th_x(b)=u', th('x','b'), 'u'), ('u=v', 'u', 'v'), ('yz=zy', th('y','z'), th('z','y'))],
 'K3b': [('th_x(c)=a', th('x','c'), 'a'), ('byb=b', th('b','y'), 'b'), ('bzb=b', th('b','z'), 'b'), ('th_y(c)=th_y(b)', th('y','c'), th('y','b')),
         ('th_z(c)=th_z(b)', th('z','c'), th('z','b')), ('th_y(z)=u', th('y','z'), 'u'), ('th_z(y)=u', th('z','y'), 'u'), ('th_x(b)=v', th('x','b'), 'v')],
 'K3c': [('bxb=b', th('b','x'), 'b'), ('th_x(a)=th_x(b)', th('x','a'), th('x','b')), ('th_x(y)=th_y(z)', th('x','y'), th('y','z')),
         ('th_z(y)=u', th('z','y'), 'u'), ('u=v', 'u', 'v'), ('zc=cz', th('z','c'), th('c','z'))],
}
name = sys.argv[1]; n = int(sys.argv[2]); cap = int(sys.argv[3]) if len(sys.argv) > 3 else 3000000
budget = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
import random; random.seed(1)
hyps = COND[name]
P = projections(n); N = len(P); idx = {p: i for i, p in enumerate(P)}
TH = [[idx[theta(P[i], P[j])] for j in range(N)] for i in range(N)]       # TH[i][j] = theta_{P_i}(P_j)
MT = [[TH[i][j] == i and TH[j][i] == j for j in range(N)] for i in range(N)]
def vars_of(t):
    if isinstance(t, str): return {'a', 'b'} if t in ('u', 'v') else {t}
    return vars_of(t[1]) | vars_of(t[2])
def ev(t, env):
    if isinstance(t, str):
        if t == 'u': return TH[env['a']][env['b']]
        if t == 'v': return TH[env['b']][env['a']]
        return env[t]
    return TH[ev(t[1], env)][ev(t[2], env)]
aux = sorted({v for h in hyps for v in vars_of(h[1]) | vars_of(h[2])} - {'a', 'b', 'c'})
# variable order: a, c, b then auxiliaries greedily
order = ['a', 'c', 'b']; rem = list(aux)
while rem:
    best = max(rem, key=lambda v: sum(1 for h in hyps if (vars_of(h[1]) | vars_of(h[2])) <= set(order + [v])))
    order.append(best); rem.remove(best)
def checks_for(hs):
    return [[h for h in hs if (vars_of(h[1]) | vars_of(h[2])) <= set(order[:i+1]) and not (vars_of(h[1]) | vars_of(h[2])) <= set(order[:i])]
            for i in range(len(order))]
def enumerate_insts(hs, cap):
    """all assignments with a><c><b and the atoms hs; returns list of env tuples (in `order`), capped."""
    chk = checks_for(hs); out = []; env = {}; t1 = time.time(); stop = [False]
    def rec(i):
        if len(out) >= cap or stop[0]: return
        if i == len(order): out.append(tuple(env[v] for v in order)); return
        v = order[i]
        if v == 'c': cands = [c for c in range(N) if MT[env['a']][c]]
        elif v == 'b': cands = [b for b in range(N) if MT[env['c']][b]]
        else: cands = range(N)
        for val in cands:
            env[v] = val
            if all((ev(h[1], env) == ev(h[2], env)) for h in chk[i]): rec(i + 1)
        del env[v]
    for (a, c, b) in TRIPLES:
        if time.time() - t1 > budget or len(out) >= cap: stop[0] = True; break
        env = {'a': a, 'c': c, 'b': b}
        if all(ev(h[1], env) == ev(h[2], env) for i in range(3) for h in chk[i]): rec(3)
    out.append(('STOPPED',) if stop[0] else ('COMPLETE',)); return out
terms = [v for v in order] + ['u', 'v'] + [th(p, q) for p in order for q in order]
tname = lambda t: t if isinstance(t, str) else 'th_%s(%s)' % (t[1], t[2])
def rows(insts):
    R = np.empty((len(insts), len(terms)), dtype=np.int32)
    for k, inst in enumerate(insts):
        env = dict(zip(order, inst))
        R[k] = [ev(t, env) for t in terms]
    return R
def ab(R):  # a><b per row
    A = R[:, 0]; B = R[:, order.index('b')]
    return np.array([MT[a][b] for a, b in zip(A, B)], dtype=bool)
TRIPLES = [(a, c, b) for a in range(N) for c in range(N) if MT[a][c] for b in range(N) if MT[c][b]]
random.shuffle(TRIPLES)
def strip(insts):
    flag = insts.pop()[0]; return insts, flag
t0 = time.time()
full, flag = strip(enumerate_insts(hyps, cap)); Rf = rows(full); okf = ab(Rf)
print('triples (a,c,b): %d, in random order; per-enumeration budget %.0fs' % (len(TRIPLES), budget))
print('%s in P_%d: order %s; full instances %d%s, violations of a><b %d (%.0fs)' % (name, n, order, len(full), ' (' + flag + ')', (~okf).sum(), time.time() - t0), flush=True)
cons = [(i, j) for i in range(len(terms)) for j in range(i + 1, len(terms)) if np.all(Rf[:, i] == Rf[:, j])]
print('consequence atoms on full instances (%d):' % len(cons))
print('  ' + '; '.join(tname(terms[i]) + '=' + tname(terms[j]) for i, j in cons), flush=True)
# dropped-hypothesis map
drop = {}
for h in hyps:
    others = [g for g in hyps if g is not h]
    insts, flag = strip(enumerate_insts(others, cap))
    R = rows(insts); hv = np.array([ev(h[1], dict(zip(order, inst))) == ev(h[2], dict(zip(order, inst))) for inst in insts])
    D = R[~hv]; okd = ab(D)
    line = '  drop %-18s dropped instances %8d%s, violations of a><b %7d' % (h[0], len(D), ' (' + flag + ')', (~okd).sum())
    # which consequence atoms survive the drop (hold on all dropped instances) and which weakenings force a><b
    surv = [(i, j) for i, j in cons if len(D) and np.all(D[:, i] == D[:, j])]
    weak = []
    for i, j in cons:
        m = D[:, i] == D[:, j]
        if m.sum() and okd[m].all() and (~m & okd).any(): weak.append((tname(terms[i]) + '=' + tname(terms[j]), int(m.sum())))
    drop[h[0]] = (len(D), int((~okd).sum()), surv, weak)
    print(line, flush=True)
    print('     atoms still valid without it: ' + ('; '.join(tname(terms[i]) + '=' + tname(terms[j]) for i, j in surv) or 'none'), flush=True)
    weak.sort(key=lambda w: -w[1])
    print('     nontrivial weakenings forcing a><b (atom, instances): ' + ('; '.join('%s [%d]' % w for w in weak[:12]) or 'none'), flush=True)
pickle.dump({'order': order, 'terms': [tname(t) for t in terms], 'cons': cons, 'drop': drop, 'nfull': len(full)}, open('recon_%s_%d.pkl' % (name, n), 'wb'))
print('done (%.0fs)' % (time.time() - t0))
