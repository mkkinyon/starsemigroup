"""Induction step for T: does T(y with partner z) + y~z, z id, z~b give T(z with partner b)?"""
import sys, time
exec(open('meets.py').read().split("L = 'abcy'")[0])
def meetst(P, Q, R): return meet(frozenset(P), frozenset(Q), frozenset(R))
def holds4(H, hyps, goal):
    T, idx = table(H, ('mt','a','b'))
    triples = sorted({tuple(sorted(a[1:])) for cl in hyps + [goal] for s_, a in cl if a[0] == 'J3'})
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}; c.J3s = {}
        for tr in triples: c.J3s[tr] = make_J3(pool, cls, E, X, tuple(idx[p] for p in tr), tr)
        for cl in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append(J3lits(c, u, v, cl))
        ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in J3lits(c, u, v, goal): cls.append([-w_, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
Tyz = meetst('az', 'cyz', 'cz')        # T for chain end y with partner z
Tzb = meetst('ab', 'bcz', 'bc')        # goal: T for chain end z with partner b
A_y = ((-1, ('E','c')), (1, ('J','a','y'))); A_z = ((-1, ('E','c')), (1, ('J','a','z')))
M_y = ((1, ('E','c')), (-1, ('J','a','c')), (-1, ('J','c','y'))); M_z = ((1, ('E','c')), (-1, ('J','a','c')), (-1, ('J','c','z')))
step = [('mt','a','c'), idf('y'), ('comm','y','z'), idf('z'), ('comm','z','b')]
tests = {
 "T(y;z) => T(z;b)": [Tyz],
 "T(y;z) + A(y) + A(z) => T(z;b)": [Tyz, A_y, A_z],
 "T(y;z) + A(y),A(z),M(y),M(z) => T(z;b)": [Tyz, A_y, A_z, M_y, M_z],
 "A(z) + M(z) => T(z;b)": [A_z, M_z],
}
for name, hy in tests.items():
    t = time.time(); print(f"m={m}: {name}: {holds4(step, hy, Tzb)} ({time.time()-t:.0f}s)", flush=True)
# sanity: with the real chain (c~y) instead of T(y;z)
real = [('mt','a','c'), ('comm','y','c'), idf('y'), ('comm','y','z'), idf('z'), ('comm','z','b')]
print(f"m={m}: real chain c~y~z, z~b => T(z;b): {holds4(real, [], Tzb)}")
