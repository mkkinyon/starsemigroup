"""K0 instances in P(P_n): a><c><b, y~c, theta_y(b)=v, theta_b(z)=b, theta_z(a)=theta_z(b), theta_y(z)=u.  Usage: python3 k0inst.py n [budget]"""
import sys, time, random, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
def instances(n, budget=1e9, seed=1):
    P = projections(n); random.seed(seed); t0 = time.time(); out = []
    pairs = [(a, c) for a in P for c in P if matched(a, c)]
    if n >= 5: random.shuffle(pairs)
    for a, c in pairs:
        if time.time() - t0 > budget: break
        Ys = [y for y in P if commute(y, c)]
        for b in P:
            if not matched(b, c): continue
            u = theta(a, b); v = theta(b, a)
            Yb = [y for y in Ys if theta(y, b) == v]
            if not Yb: continue
            for z in P:
                if theta(b, z) != b or theta(z, a) != theta(z, b): continue
                for y in Yb:
                    if theta(y, z) == u: out.append({'a': a, 'b': b, 'c': c, 'y': y, 'z': z})
    return out
if __name__ == '__main__':
    n = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 1e9
    I = instances(n, budget); print(len(I), 'instances'); pickle.dump(I, open("k0inst%d.pkl" % n, "wb")); print("a!=b:", sum(1 for d in I if d["a"]!=d["b"]))
    bad = sum(1 for d in I if not matched(d['a'], d['b'])); print('violations of a><b:', bad)
