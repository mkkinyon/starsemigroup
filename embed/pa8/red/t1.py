import sys
exec(open('meets.py').read().split("L = 'abcy'")[0])
def meetst(P, Q, R): return meet(frozenset(P), frozenset(Q), frozenset(R))
def holds3(H, hyps, goal):
    T, idx = table(H, ('mt','a','b'))
    letters = sorted({p for s_, a in goal for p in a[1:] if a[0] in ('J','J3')} | {'a','b','c'})
    triples = [tuple(sorted(a[1:])) for s_, a in goal if a[0] == 'J3']
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in idx if isinstance(k, str)}; c.J3s = {}
        for tr in triples: c.J3s[tr] = make_J3(pool, cls, E, X, tuple(idx[p] for p in tr), tr)
        ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in J3lits(c, u, v, goal): cls.append([-w_, -l])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra) is None
one = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','b')]
two = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
three = two[:-1] + [('comm','y','z'), idf('z'), ('comm','z','b')]
# rename: for 'one' the chain end is x; for 'two' it is y; for 'three' it is z.
tests = [("T1: (ab)^(bcx) <= (bc)", one, meetst('ab','bcx','bc')),
         ("T2: (ab)^(bcy) <= (bc)", two, meetst('ab','bcy','bc')),
         ("T3: (ab)^(bcz) <= (bc)", three, meetst('ab','bcz','bc')),
         ("T1': (ab)^(bx) <= (b)", one, meetst('ab','bx','b')),
         ("T2': (ab)^(by) <= (b)", two, meetst('ab','by','b')),
         ("T3': (ab)^(bz) <= (b)", three, meetst('ab','bz','b')),
         ("U1: (ac)^(bcx) <= (c)", one, meetst('ac','bcx','c')),
         ("U2: (ac)^(bcy) <= (c)", two, meetst('ac','bcy','c')),
         ("V2: (acy)^(bcy) <= (cy)", two, meetst('acy','bcy','cy')),
         ("W2: (aby)^(acy) <= (ay)", two, meetst('aby','acy','ay')),
         ("W1: (abx)^(acx) <= (ax)", one, meetst('abx','acx','ax')),
         ]
for name, H, g in tests:
    print(f"m={m}: {name}: {holds3(H, [], g)}", flush=True)
