import sys, time, itertools
sys.argv = ['x', sys.argv[1]]
exec(open('lemA_dec.py').read().split("base1 = ")[0])
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
base3 = base2 + [('comm','y','z'), idf('z')]
valid2 = ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'ac_le_ap', 'cp_le_ap', 'pAC', 'aCP', 'Np_unionC']
step3 = [('mt','a','c'), idf('y'), ('comm','y','z'), idf('z')]
print(f"m={m}: all 13 position-2 statements for y + y~z + z id => A(z): {run(step3, [(q, 'y') for q in valid2], ('A', 'z'))}", flush=True)
# pair statements about (x, y) [x = previous, p = current]; test validity at (1,2) [base2, p=y] and (2,3) [base3 with x:=y, p=z -- need renaming]
# we implement pair predicates with explicit names q (previous) and p (current)
PAIR = {
 'Np_cblock_rel': lambda c, q, p, u, v: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), c.Tl(c.i['c'], u), c.Tl(c.i[q], u), c.E(c.i['c'], u, v)],   # N(p)-block with a point outside supp c u supp q lies in one c-block
 'Np_in_qc': lambda c, q, p, u, v: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), c.J(c.i['c'], c.i[q], u, v)],                              # N(p)-block lies in one class of c v q
 'p_le_qa': lambda c, q, p, u, v: [-c.E(c.i[p], u, v), c.J(c.i['a'], c.i[q], u, v)],                                                 # p-blocks lie in classes of q v a
 'Np_le_qc_or_c': lambda c, q, p, u, v: [-c.E(c.i[p], u, v), c.Tl(c.i[p], u), c.Tl(c.i['c'], u), c.J(c.i['c'], c.i[q], u, v)],
 'c_le_pq': lambda c, q, p, u, v: [-c.E(c.i['c'], u, v), c.J(c.i[p], c.i[q], u, v)],                                                  # c-blocks in classes of p v q
}
def runpair(H, hyps, goal):
    """hyps/goal: (name, q, p)"""
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}
        for name, q, p in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append(PAIR[name](c, q, p, u, v))
        name, q, p = goal; ors = []
        for u in X:
            for v in X:
                if u != v:
                    s = pool.id(('neg', u, v)); ors.append(s)
                    for l in PAIR[name](c, q, p, u, v): cls.append([-s, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
for nm in PAIR:
    v12 = runpair(base2, [], (nm, 'x', 'y')); v23 = runpair(base3, [], (nm, 'y', 'z')); v01 = runpair([('mt','a','c'), ('comm','x','c'), idf('x')], [], (nm, 'c', 'x'))
    print(f"m={m}: pair [{nm}]: at (c,x): {v01}, at (x,y): {v12}, at (y,z): {v23}", flush=True)
