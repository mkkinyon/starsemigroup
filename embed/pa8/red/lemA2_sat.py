"""Inductive form of Lemma A: does 'every c-block lies in one class of eps_x v eps_a' propagate along x ~ y when y identifies a with c?
Usage: python3 lemA2_sat.py m"""
import sys, time
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import table
from pa_sat import solve
def test(H, hypblocks, m):
    """hypblocks: list of (p, q1, q2): every block of p lies in one class of eps_q1 v eps_q2 (as hypothesis); refute the same for ('c','y','a')"""
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
                    cls.append([-w, E(idx['c'], x, y)]); cls.append([-w, -J(idx['y'], idx['a'], x, y)])
        cls.append(ors)
    return solve(T, m, distinct=False, verbose=False, symbreak=False, extra=extra)
m = int(sys.argv[1])
base = [('mt', 'a', 'c'), ('comm', 'x', 'y'), ('eq', ('y', 'a'), ('y', 'c'))]
cases = {
 "A':  x id + [c-blocks in classes of x v a] + x~y + y id": (base + [('eq', ('x', 'a'), ('x', 'c'))], [('c', 'x', 'a')]),
 "A'': [c-blocks in classes of x v a] + x~y + y id (no x id)": (base, [('c', 'x', 'a')]),
 "A''': x id + x~y + y id (no block hyp)": (base + [('eq', ('x', 'a'), ('x', 'c'))], []),
 "A (orig): x~c + x id + x~y + y id": (base + [('comm', 'x', 'c'), ('eq', ('x', 'a'), ('x', 'c'))], []),
}
for name, (H, hb) in cases.items():
    t = time.time(); r = test(H, hb, m)
    print(f"m={m} {name}: {'HOLDS' if r is None else 'FAILS'} ({time.time()-t:.0f}s)", flush=True)
