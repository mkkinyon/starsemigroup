"""Instances of (R'_2) in P_n: a|><|c|><|b, x1~c, x1~x2, th_x1(a)=th_x1(c), th_x2(a)=th_x2(c), y~a, th_x2(b)=th_y(b).  Stored as (a,c,b,x1,x2,y)."""
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
        Id = [x for x in P if th(x, a) == th(x, c)]
        X1 = [x for x in Id if comm(x, c)]
        Ya = [y for y in P if comm(y, a)]
        for x1 in X1:
            X2 = [x for x in Id if comm(x, x1)]
            for x2 in X2:
                for b in Bs:
                    r = th(x2, b)
                    for y in Ya:
                        if th(y, b) == r: inst.append((a, c, b, x1, x2, y))
print("n =", n, "instances:", len(inst), f"({time.time()-t0:.0f}s)", flush=True)
pickle.dump(inst, open(f'rp2inst{n}.pkl', 'wb'))
print("conclusion fails in", sum(1 for I in inst if not matched(I[0], I[2])))
print("all distinct:", sum(1 for I in inst if len(set(I)) == 6))
