import sys, time, pickle
exec(open('goal2.py').read().split("t = time.time()")[0])
Qx = pickle.load(open('invQ_m5.pkl', 'rb'))
def renx(cl):
    out = []
    for s, a in cl:
        a = tuple('y' if p == 'x' else p for p in a) if a[0] != 'T' else (a[0], 'y' if a[1] == 'x' else a[1], a[2])
        if a[0] == 'J' and a[1] > a[2]: a = ('J', a[2], a[1])
        out.append((s, a))
    return tuple(out)
Qy = [renx(cl) for cl in Qx]
A_y = ((-1, ('E','c')), (1, ('J','a','y')))
M_y = ((1, ('E','c')), (-1, ('J','a','c')), (-1, ('J','c','y')))
G2p_y = ((-1, ('J3','a','c','y')), (-1, ('T','c','u')), (-1, ('T','c','v')), (1, ('J','c','y')))
G2pa_y = ((-1, ('J3','a','c','y')), (-1, ('T','a','u')), (-1, ('T','a','v')), (1, ('J','a','y')))
G1 = ((-1, ('E', 'c')), (1, ('J', 'a', 'b')))
TR = [('a','b','c'), ('a','c','y')]
def holds2(H, hyps, goal):
    T, idx = table(H, ('mt','a','b'))
    def extra(pool, E, Tl, J, cls, X):
        c = mkctx(pool, cls, E, Tl, J, X, idx, TR)
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
I = [A_y, M_y, G2p_y, G2pa_y]
for name, hy in (("A+M+G2'+G2'a", I), ("A+M+G2'+G2'a+Q20", I + Qy), ("G2' only", [G2p_y]), ("A+G2'", [A_y, G2p_y])):
    t = time.time(); print(f"m={m}: weak + {name}(y) => G1: {holds2(weak, hy, G1)}; => GOAL: {holds2(weak, hy, GOAL)} ({time.time()-t:.0f}s)", flush=True)
