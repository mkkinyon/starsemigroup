import sys
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
exec(open('inv2.py').read().split("def clauses():")[0].replace("m = int(sys.argv[1]); K = int(sys.argv[2])", "m = int(sys.argv[1])"))
from qi import table
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
base2 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')]
def cex(H, goal):
    T, idx = table(H, ('mt','a','c'))
    def extra(pool, E, Tl, J, cls, X):
        c = Ctx(); c.E, c.Tl, c.J = E, Tl, J; cl, ren = goal; r = ren or {}
        c.i = {k: idx[r.get(k, k)] for k in V if r.get(k, k) in idx}; ors = []
        for u in X:
            for v in X:
                if u != v:
                    w_ = pool.id(('neg', u, v)); ors.append(w_)
                    for l in cl: cls.append([-w_, -lit_val(c, u, v, l)])
        cls.append(ors)
    r = solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra)
    if r:
        for v in ['a','c','x','y']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,b)) + (']' if k=='T' else ')') for b,k in r[idx[v]]))
    else: print('  none')
alpha = ((-1, ('E','x')), (-1, ('T','x','u')), (1, ('T','c','v')))   # placeholder, built below
# (alpha'): ~E(y) | ~T(c,u) | T(c,v)   with predicate variable x renamed to y
cl_alpha = ((-1, ('E','x')), (-1, ('T','c','u')), (1, ('T','c','v')))
cl_beta = ((-1, ('E','x')), (1, ('T','c','u')), (1, ('E','c')))
print("counterexample to (alpha') at position 2:"); cex(base2, (cl_alpha, {'x': 'y'}))
print("counterexample to (beta) at position 2:"); cex(base2, (cl_beta, {'x': 'y'}))
