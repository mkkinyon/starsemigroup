import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
def test(H, concl_pq, m, hypblocks=()):
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
                    cls.append([-w, E(idx['c'], x, y)]); cls.append([-w, -J(idx[concl_pq[0]], idx[concl_pq[1]], x, y)])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra)
m = int(sys.argv[1])
idf = lambda v: ('eq', (v, 'a'), (v, 'c'))
chain3 = [('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y'), ('comm','y','z'), idf('z')]
cases = {
 "A3: c~x~y~z all id => c-blocks in classes of z v a": (chain3, ('z','a'), ()),
 "A3 without z id": (chain3[:-1], ('z','a'), ()),
 "B2: c~x~y, x,y id => c-blocks in classes of y v x": ([('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')], ('y','x'), ()),
 "B2': => c-blocks in classes of y v c": ([('mt','a','c'), ('comm','x','c'), idf('x'), ('comm','x','y'), idf('y')], ('y','c'), ()),
 "A' + [c-blocks in classes of x v c] + x id + x~y + y id => y v a": ([('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')], ('y','a'), [('c','x','a'), ('c','x','c')]),
}
for name, (H, pq, hb) in cases.items():
    t = time.time(); r = test(H, pq, m, hb)
    print(f"m={m} {name}: {'HOLDS' if r is None else 'FAILS'} ({time.time()-t:.0f}s)", flush=True)
