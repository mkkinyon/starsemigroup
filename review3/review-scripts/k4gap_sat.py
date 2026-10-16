"""SAT search in P(P_m) for the K4 hypotheses together with the NEGATION of the Step-2 claim of Thm 5.49
('every B_i lies in some S_j', i.e. supp theta_b(a) = supp b).  Optional rank restrictions.
Usage: python3 k4gap_sat.py m [--rank1] [--n0] [--symbreak]
  --rank1 : all T-points of a lie in one block (rank a <= 1); a has a T-point
  --n0    : u = theta_a(b) has no T-point (rank u = 0)
A SAT answer would be a counterexample to Theorem 5.49 (and to K4) in P_m; UNSAT = the claim holds in P(P_m)."""
import sys, time, os
sys.path.insert(0, '/home/claude/pa8w/review3/code')
os.environ['EMBED_DIR'] = '/home/claude/pa8w/review3/code'
from pa_sat import solve
from qi import table
m = int(sys.argv[1])
K4 = [('mt', 'a', 'c'), ('mt', 'c', 'b'), ('fix', 'a', 'y'), ('le', 'b', 'z'), ('comm', 'y', 'c'), ('eq', ('z', 'y'), ('b', 'a')), ('eq', ('z', 'a'), ('a', 'b'))]
T, idx = table(K4, ('mt', 'a', 'b'))
N = len(T)
a, b, c, y, z = idx['a'], idx['b'], idx['c'], idx['y'], idx['z']
v = T[a][b]; u = T[b][a]   # T[q][p] = theta_p(q): v = theta_b(a), u = theta_a(b)
assert T[y][z] == v and T[a][z] == u
print('table indices:', idx, 'v =', v, 'u =', u, 'N =', N)
for i in range(N): print('  ', T[i])

def extra(pool, E, Tl, J, cls, X):
    # negation of the claim: some x with Tl(b,x) and not Tl(v,x)
    ds = []
    for x in X:
        d = pool.id(('gap', x)); ds.append(d)
        cls.append([-d, Tl(b, x)]); cls.append([-d, -Tl(v, x)])
    cls.append(ds)
    if '--rank1' in sys.argv:
        for x in X:
            for yy in X:
                if x < yy: cls.append([-Tl(a, x), -Tl(a, yy), E(a, x, yy)])
        cls.append([Tl(a, x) for x in X])
    if '--n0' in sys.argv:
        for x in X: cls.append([-Tl(u, x)])

t0 = time.time()
r = solve(T, m, distinct=False, verbose=True, symbreak=('--symbreak' in sys.argv), extra=extra)
print('m=%d: %s (%.0fs)' % (m, 'SAT -- COUNTEREXAMPLE' if r else 'UNSAT (claim holds in P(P_%d))' % m, time.time() - t0), flush=True)
if r:
    names = {i: n for n, i in idx.items()}
    for p, blocks in enumerate(r):
        print(names.get(p, 'elt%d' % p), ' '.join(('[%s]' if lab == 'T' else '(%s)') % ' '.join(map(str, bl)) for bl, lab in blocks))
