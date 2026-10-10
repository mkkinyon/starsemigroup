"""Closing lemmas: replace c~x by the block property [every c-block lies in one class of eps_x v eps_a]."""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
def valid_mt(H, m, hypblocks, concl=('a','b')):
    """is a|><|b forced?  (two SAT calls as in qi.valid, with the block hypotheses added)"""
    T, idx = table(H, ('mt',) + concl); N = len(T)
    def extra(pool, E, Tl, J, cls, X):
        for (p, q1, q2) in hypblocks:
            for x in X:
                for y in X:
                    if x < y: cls.append([-E(idx[p], x, y), J(idx[q1], idx[q2], x, y)])
    for (q, p) in ((concl[1], concl[0]), (concl[0], concl[1])):   # theta_p(q) != q
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
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
P = [('mt','a','c'), ('mt','c','b')]
cases = {
 "(R)' with c~x replaced by [c in x v a]:  x~b, x id": (P + [('comm','x','b'), idf('x')], [('c','x','a')]),
 "(R)' with c~x replaced by [c in x v a] and [a in x v c]": (P + [('comm','x','b'), idf('x')], [('c','x','a'), ('a','x','c')]),
 "(R') with c~x replaced by [c in x v a]: x id, y~a, th_x(b)=th_y(b)": (P + [idf('x'), ('comm','y','a'), ('eq',('x','b'),('y','b'))], [('c','x','a')]),
 "(R') with [c in x v a],[a in x v c]": (P + [idf('x'), ('comm','y','a'), ('eq',('x','b'),('y','b'))], [('c','x','a'), ('a','x','c')]),
 "(R)' original": (P + [('comm','x','c'), ('comm','x','b'), idf('x')], []),
}
m = int(sys.argv[1])
for name, (H, hb) in cases.items():
    t = time.time(); r = valid_mt(H, m, hb); print(f"m={m} {name}: {'VALID' if r else 'FAILS'} ({time.time()-t:.0f}s)", flush=True)
