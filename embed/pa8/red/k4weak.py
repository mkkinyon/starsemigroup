"""Weakening search for K4 in P(P_4): for h in {y~c, th_z(y)=v, th_z(a)=u}, which atoms s=t (s,t among
a,b,c,y,z and theta_p(q), p,q in {a,b,c,y,z}) are (i) true on all K4 instances and (ii) such that a><b holds on
all instances satisfying the other hypotheses and the atom but not h?  (aya=a and b<=z cannot be weakened: every
instance lacking only one of them violates a><b, k4drop.py.)  Usage: python3 k4weak.py"""
import sys, time, itertools, pickle
import numpy as np
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
n = 4; P = projections(n); idx = {p: i for i, p in enumerate(P)}
le = lambda p, q: theta(q, p) == p
V = ['a', 'b', 'c', 'y', 'z']
terms = [(v,) for v in V] + [(p, q) for p in V for q in V]          # (p,q) = theta_p(q)
names = [t[0] for t in terms[:5]] + ['th_%s(%s)' % t for t in terms[5:]]
def row(a, b, c, y, z):
    env = dict(a=a, b=b, c=c, y=y, z=z)
    return [idx[env[t[0]]] if len(t) == 1 else idx[theta(env[t[0]], env[t[1]])] for t in terms]
t0 = time.time()
full = []; drop = {'y~c': [], 'th_z(y)=v': [], 'th_z(a)=u': []}; viol = {k: [] for k in drop}
pairs = [(a, c) for a in P for c in P if matched(a, c)]
for a, c in pairs:
    Ya = [y for y in P if theta(a, y) == a]
    Y = [y for y in Ya if commute(y, c)]
    for b in P:
        if not matched(b, c): continue
        u = theta(a, b); v = theta(b, a); ok = matched(a, b)
        Zb = [z for z in P if le(b, z)]
        Z = [z for z in Zb if theta(z, a) == u]
        for z in Z:
            for y in Y:
                if theta(z, y) == v: full.append(row(a, b, c, y, z))
                else: drop['th_z(y)=v'].append(row(a, b, c, y, z)); viol['th_z(y)=v'].append(not ok)
            for y in Ya:
                if theta(z, y) == v and not commute(y, c): drop['y~c'].append(row(a, b, c, y, z)); viol['y~c'].append(not ok)
        for z in Zb:
            if theta(z, a) == u: continue
            for y in Y:
                if theta(z, y) == v: drop['th_z(a)=u'].append(row(a, b, c, y, z)); viol['th_z(a)=u'].append(not ok)
F = np.array(full); print('full', len(F), '(%.0fs)' % (time.time() - t0))
T = len(terms); cons = [(i, j) for i in range(T) for j in range(i + 1, T) if np.all(F[:, i] == F[:, j])]
print(len(cons), 'consequence atoms on the full instances')
out = {}
for h in drop:
    D = np.array(drop[h]); W = np.array(viol[h]); print('drop', h, len(D), 'instances,', W.sum(), 'violations')
    res = []
    for i, j in cons:
        m = D[:, i] == D[:, j]
        if m.sum() == 0: continue             # atom equivalent to h on the dropped set
        if W[m].sum() == 0: res.append((names[i] + ' = ' + names[j], int(m.sum())))
    res.sort(key=lambda r: -r[1]); out[h] = res
    print('  weakenings (atom, surviving dropped instances with a><b):')
    for r in res: print('    %-32s %7d' % r)
pickle.dump({'terms': names, 'cons': [(names[i], names[j]) for i, j in cons], 'out': out}, open('k4weak4.pkl', 'wb'))
