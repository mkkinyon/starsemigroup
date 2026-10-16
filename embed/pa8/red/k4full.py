"""K4 counterexample search in P(P_m) with supp z = X (restricted setting).  Usage: python3 k4full.py m"""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
m = int(sys.argv[1])
K4 = [('mt','a','c'), ('mt','c','b'), ('fix','a','y'), ('le','b','z'), ('comm','y','c'), ('eq',('z','y'),('b','a')), ('eq',('z','a'),('a','b'))]
T, idx = table(K4, ('mt','a','b'))
ia, ib, iz = idx['a'], idx['b'], idx['z']; iu = T[ib][ia]
def extra(pool, E, Tl, J, cls, X):
    for x in X: cls.append([Tl(iz, x)])          # supp z = X
    # deny theta_a(b) = a : u != a  (some point differs in label or relation)
    ds = []
    for x in X:
        d = pool.id(('du', x)); ds.append(d); cls.append([-d, Tl(ia, x), Tl(iu, x)]); cls.append([-d, -Tl(ia, x), -Tl(iu, x)])
        for y in X:
            if y > x:
                d = pool.id(('de', x, y)); ds.append(d); cls.append([-d, E(ia, x, y), E(iu, x, y)]); cls.append([-d, -E(ia, x, y), -E(iu, x, y)])
    cls.append(ds)
t = time.time(); r = solve(T, m, distinct=False, verbose=True, symbreak=False, extra=extra)
print('m=%d, supp z = X: %s (%.0fs)' % (m, 'COUNTEREXAMPLE ' + str(r) if r else 'none', time.time() - t), flush=True)
