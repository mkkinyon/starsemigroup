import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
def test(H, concl, m, hypblocks=()):
    """concl = (p, q1, q2): refute 'every p-block lies in one class of eps_q1 v eps_q2'"""
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
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra)
m = int(sys.argv[1])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
one = [('mt','a','c'), ('comm','x','c'), idf('x')]
two = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
cases = {
 "I-a: c~x, x id => a-blocks in classes of x v c": (one, ('a','x','c'), ()),
 "I-c: c~x, x id => c-blocks in classes of x v a": (one, ('c','x','a'), ()),
 "prop: [a in x v c],[c in x v a], x id, x~y, y id => c in y v a": (two, ('c','y','a'), [('a','x','c'), ('c','x','a')]),
 "prop: same => a in y v c": (two, ('a','y','c'), [('a','x','c'), ('c','x','a')]),
 "prop2: [a in x v c],[c in x v a], x~y, y id (no x id) => c in y v a": ([('mt','a','c'), ('comm','x','y'), idf('y')], ('c','y','a'), [('a','x','c'), ('c','x','a')]),
}
for name, (H, pq, hb) in cases.items():
    t = time.time(); r = test(H, pq, m, hb)
    print(f"m={m} {name}: {'HOLDS' if r is None else 'FAILS'} ({time.time()-t:.0f}s)", flush=True)
