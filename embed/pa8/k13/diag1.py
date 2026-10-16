"""Full atom diagram of candidate 1's K1c instance (a,c,b,x,y,z) = (4,0,8,1,2,5), and structure-first minimisation
under SAT validity in P(P_4) of the condition  diagram => a><b."""
import json, sys, itertools, time, random
sys.path.insert(0, '/home/claude/pa8w/n4'); sys.path.append('/home/claude/pa8w/embed')
from qi import valid
T = json.load(open('../cand9.json'))[1]; th = lambda p, q: T[q][p]
V = {'a': 4, 'c': 0, 'b': 8, 'x': 1, 'y': 2, 'z': 5}
names = list(V)
terms = {v: V[v] for v in names}
for p in names:
    for q in names:
        if p != q: terms['th_%s(%s)' % (p, q)] = th(V[p], V[q])
def qi_term(s):
    if s in V: return s
    return (s[3], s[5])
# atoms: equalities among terms with equal value; classify
atoms = []
items = list(terms.items())
for (s, vs), (t, vt) in itertools.combinations(items, 2):
    if vs == vt: atoms.append((s, t))
def kind(s, t):
    ts, tt = qi_term(s), qi_term(t)
    if isinstance(ts, str) and isinstance(tt, tuple):
        if tt[0] == ts: return 'half ' + s + '=' + t          # th_s(q) = s
        if tt[1] == ts: return 'order ' + s + '<=' + tt[0]      # th_p(s) = s
    if isinstance(ts, tuple) and isinstance(tt, tuple) and ts == (tt[1], tt[0]): return 'comm %s~%s' % ts
    if isinstance(ts, tuple) and isinstance(tt, tuple) and ts[0] == tt[0]: return 'ident %s: %s=%s' % (ts[0], ts[1], tt[1])
    return 'eq ' + s + '=' + t
A = [(kind(s, t), ('eq', qi_term(s), qi_term(t))) for s, t in atoms]
print(len(A), 'atoms in the diagram; by kind:', {k: sum(1 for a in A if a[0].startswith(k)) for k in ('half', 'order', 'comm', 'ident', 'eq')})
path = [('mt', 'a', 'c'), ('mt', 'c', 'b')]; concl = ('mt', 'a', 'b')
t0 = time.time(); print('full diagram valid at m=4:', valid(path + [a[1] for a in A], concl, 4), '(%.0fs)' % (time.time() - t0), flush=True)
# structure-first greedy minimisation: try to remove 'eq' atoms first, then 'ident', then 'comm', 'order', 'half'
prio = {'eq': 0, 'ident': 1, 'comm': 2, 'order': 3, 'half': 4}
order = sorted(range(len(A)), key=lambda i: (prio[A[i][0].split()[0]], random.random()))
keep = set(range(len(A)))
for i in order:
    trial = [A[j][1] for j in sorted(keep - {i})]
    if valid(path + trial, concl, 5): keep.discard(i)
print('minimal (structure-first) hypothesis set, %d atoms:' % len(keep))
for i in sorted(keep, key=lambda i: prio[A[i][0].split()[0]]): print('   ', A[i][0])
for m in (6,):
    t0 = time.time(); print('valid at m=%d:' % m, valid(path + [A[i][1] for i in keep], concl, m), '(%.0fs)' % (time.time() - t0), flush=True)
