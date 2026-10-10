"""Fixed point of propagation for the clause invariant, then the closing lemmas.  Usage: python3 inv3.py m pklfile"""
import sys, time, pickle
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
exec(open('inv2.py').read().split("def clauses():")[0].replace("m = int(sys.argv[1]); K = int(sys.argv[2])", "m = int(sys.argv[1])"))
from qi import table
S1, S2, S3 = pickle.load(open(sys.argv[2], 'rb'))
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
baseP = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
Q = list(S3); t0 = time.time()
while True:
    good = [cl for cl in Q if run(baseP, [(c2, None) for c2 in Q], (cl, {'x': 'y'}))]
    print(f"m={m}: {len(good)} of {len(Q)} propagate ({time.time()-t0:.0f}s)", flush=True)
    if len(good) == len(Q): break
    Q = good
print("invariant Q (fixed point):")
for cl in Q: print('   ', fmt(cl))
# base case: Q holds for x when c~x, x id  (it does, Q subset of S1) -- recheck at this m
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
print("base case at this m:", all(run(base1, [], (cl, None)) for cl in Q), flush=True)
# closing: Q(x), x~b, b|><|c  =>  a|><|b ?   and the (R') closing
def valid_mt(H, hyps, concl=('a','b')):
    T, idx = table(H, ('mt',) + concl); N = len(T)
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in V}
        for cl, ren in hyps:
            for u in X:
                for v in X:
                    if u != v: cls.append([lit_val(c, u, v, l) for l in cl])
    for (q, p) in ((concl[1], concl[0]), (concl[0], concl[1])):
        T2 = [row[:] + [None] for row in T] + [[None] * (N + 1)]
        for i in range(N + 1): T2[i][i] = i
        w = T2[idx[q]][idx[p]]
        if w is not None:
            if w == idx[p]: continue
            if solve(T, m, distinct=[(w, idx[p])], verbose=False, symbreak=False, extra=extra) is not None: return False
            continue
        T2[idx[q]][idx[p]] = N
        if solve(T2, m, distinct=[(N, idx[p])], verbose=False, symbreak=False, extra=extra) is not None: return False
    return True
P = [('mt','a','c'), ('mt','c','b')]
hy = [(cl, None) for cl in Q]
t = time.time(); print("closing (W): Q(x), x id, x~b, b|><|c => a|><|b:", valid_mt(P + [idf('x'), ('comm','x','b')], hy), f"({time.time()-t:.0f}s)", flush=True)
t = time.time(); print("closing (R'): Q(x), x id, y~a, th_x(b)=th_y(b) => a|><|b:", valid_mt(P + [idf('x'), ('comm','y','a'), ('eq',('x','b'),('y','b'))], hy), f"({time.time()-t:.0f}s)", flush=True)
pickle.dump(Q, open(f'invQ_m{m}.pkl', 'wb'))
