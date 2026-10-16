"""Targeted search for a K4 counterexample in P(P_m) with rk a = M, rk u = N (< M).  Usage: python3 k4rank.py m M N"""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
from pysat.card import CardEnc, EncType
m, M, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
K4 = [('mt','a','c'), ('mt','c','b'), ('fix','a','y'), ('le','b','z'), ('comm','y','c'), ('eq',('z','y'),('b','a')), ('eq',('z','a'),('a','b'))]
T, idx = table(K4, ('mt','a','b'))
ia, ib = idx['a'], idx['b']; iu = T[ib][ia]; iv = T[ia][ib]
assert iu is not None and iv is not None
def extra(pool, E, Tl, J, cls, X):
    def reps(p):
        out = []
        for x in X:
            r = pool.id(('rep', p, x)); out.append(r)
            cls.append([-r, Tl(p, x)])
            for y in X:
                if y < x: cls.append([-r, -E(p, y, x)])
            cls.append([r, -Tl(p, x)] + [E(p, y, x) for y in X if y < x])
        return out
    for p, bound in ((ia, M), (iu, N)):
        enc = CardEnc.equals(lits=reps(p), bound=bound, top_id=pool.top, encoding=EncType.seqcounter)
        pool.occupy(pool.top + 1, enc.nv); cls.extend(enc.clauses)
t = time.time(); r = solve(T, m, distinct=False, verbose=True, symbreak=False, extra=extra)
print('m=%d rk a=%d rk u=%d: %s (%.0fs)' % (m, M, N, 'COUNTEREXAMPLE ' + str(r) if r else 'none', time.time() - t), flush=True)
