import sys, time, pickle
sys.argv = ['x', sys.argv[1], '3']
exec(open('inv5.py').read().split("t0 = time.time(); S = []")[0])
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb'))
t0 = time.time()
S5 = [cl for cl in S if run(W2, cl)]; new5 = [cl for cl in new if cl in S5]
print(f"m={m}: {len(S5)} of {len(S)} clauses still valid under (W_2); {len(new5)} of the {len(new)} x-link clauses ({time.time()-t0:.0f}s)", flush=True)
for cl in new:
    if cl not in S5: print('   lost at this m:', fmt(cl))
# closing: weak hypotheses + all valid clauses => a |><| b ?
def valid_mt(H, hyps, concl=('a','b')):
    T, idx = table(H, ('mt',) + concl); N = len(T)
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; c.i = {k: idx[k] for k in V}
        for cl in hyps:
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
t0 = time.time(); print(f"m={m}: closing from the local clauses (weak hyps + all {len(S5)} clauses) => a|><|b:", valid_mt(weak, S5), f"({time.time()-t0:.0f}s)", flush=True)
t0 = time.time(); print(f"m={m}: closing from the x-link clauses only (weak hyps + {len(new5)} clauses):", valid_mt(weak, new5), f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump((S5, new5), open(f'inv5_m{m}_K3_checked.pkl', 'wb'))
