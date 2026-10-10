import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
def test(H, concl, m, hypblocks=()):
    T, idx = table(H, ('mt', 'a', 'c'))
    def extra(pool, E, Tl, J, cls, X):
        for (p, q1, q2) in hypblocks:
            for x in X:
                for y in X:
                    if x < y: cls.append([-E(idx[p], x, y), J(idx[q1], idx[q2], x, y)])
        ors = []
        for x in X:
            for y in X:
                if x < y:
                    w = pool.id(('neg', x, y)); ors.append(w)
                    cls.append([-w, E(idx[concl[0]], x, y)]); cls.append([-w, -J(idx[concl[1]], idx[concl[2]], x, y)])
        cls.append(ors)
    r = solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra)
    return r, idx
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
H = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
for m in (3, 4):
    r, idx = test(H, ('c','y','a'), m, [('c','x','a')])
    if r:
        print(f"counterexample m={m}:")
        for v in ['a','c','x','y']:
            print(f"  {v:2s}", '  '.join(('[' if k=='T' else '(') + ' '.join(map(str,b)) + (']' if k=='T' else ')') for b,k in r[idx[v]]))
        break
