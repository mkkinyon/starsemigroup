"""Enumerate instances of the hypotheses of (R'') in P_n: a~c, b~c, xc=cx, xax=xcx, yb=by, xbx=yay."""
import sys, time, pickle
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = int(sys.argv[1]); P = projections(n); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
def matched(p, q): return th(p, q) == p and th(q, p) == q
def comm(p, q): return m(p, q) == m(q, p)
t0 = time.time(); inst = []
for a in P:
    for c in P:
        if not matched(a, c): continue
        Bs = [b for b in P if matched(b, c)]
        Xs = [x for x in P if comm(x, c) and th(x, a) == th(x, c)]
        for x in Xs:
            for b in Bs:
                rb = th(x, b)
                for y in P:
                    if comm(y, b) and th(y, a) == rb: inst.append((a, c, b, x, y))
print("n =", n, "instances:", len(inst), f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump(inst, open(f'inst{n}.pkl', 'wb'))
print("conclusion fails in", sum(1 for I in inst if not matched(I[0], I[2])))
print("a,b,c,x,y distinct:", sum(1 for I in inst if len(set(I)) == 5))
