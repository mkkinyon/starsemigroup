"""Does the obstruction of 5.14(h) occur: a T(y)-block meeting two distinct T(b)-blocks, under the (W_2) hypotheses?  Print an instance."""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
W2 = [('mt','a','c'), ('mt','c','b'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','b')]
def find(H, m, extra_hyp=None):
    T, idx = table(H, ('mt','a','b'))
    def extra(pool, E, Tl, J, cls, X):
        ors = []
        for u in X:
            for v in X:
                if u < v:
                    w = pool.id(('ob', u, v)); ors.append(w)
                    # u, v in the same T(y)-block, both in supp b, different b-blocks
                    cls.append([-w, E(idx['y'], u, v)]); cls.append([-w, Tl(idx['y'], u)])
                    cls.append([-w, Tl(idx['b'], u)]); cls.append([-w, Tl(idx['b'], v)]); cls.append([-w, -E(idx['b'], u, v)])
        cls.append(ors)
        if extra_hyp: extra_hyp(pool, E, Tl, J, cls, X, idx)
    return solve(T, m, distinct=True, verbose=False, symbreak=False, extra=extra), idx
for m in (3, 4, 5):
    t = time.time(); r, idx = find(W2, m)
    print(f"m={m}: {'instance found' if r else 'none'} ({time.time()-t:.0f}s)", flush=True)
    if r:
        for v in ['a','c','b','x','y']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,bl)) + (']' if k=='T' else ')') for bl,k in r[idx[v]]))
        break
