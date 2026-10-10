"""Sampled W_2 instances in P_5: random matched pairs (a,c), all b, x, y."""
import sys, time, pickle, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 5; P = projections(n); random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
NP = int(sys.argv[2]) if len(sys.argv) > 2 else 40
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
def matched(p, q): return th(p, q) == p and th(q, p) == q
def comm(p, q): return m(p, q) == m(q, p)
t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and matched(a, c)]
print("matched pairs (a!=c):", len(pairs), f"({time.time()-t0:.0f}s)", flush=True)
random.shuffle(pairs); pairs = pairs[:NP]
inst = []
for a, c in pairs:
    Bs = [b for b in P if matched(b, c)]
    Xs = [x for x in P if comm(x, c) and th(x, a) == th(x, c)]
    Ys = [y for y in P if th(y, a) == th(y, c)]
    for b in Bs:
        Yb = [y for y in Ys if comm(y, b)]
        for x in Xs:
            for y in Yb:
                if comm(x, y): inst.append((a, c, b, x, y))
    print(len(inst), f"({time.time()-t0:.0f}s)", flush=True)
print("instances:", len(inst), "conclusion fails:", sum(1 for I in inst if not matched(I[0], I[2])))
pickle.dump(inst, open(f'w2inst5_s{sys.argv[1] if len(sys.argv)>1 else 0}.pkl', 'wb'))
