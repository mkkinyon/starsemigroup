"""(T_n) in the inequality form: (e_a v e_b) ^ (e_b v e_c v e_xn) <= e_b v e_c, b arbitrary commuting with x_n.
Exhaustive in P_4 for n = 1, 2; random in P_5."""
import sys, random, time
from fast import *
m = int(sys.argv[1]); nmax = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else 'all'
P = projections(m)
def classes(*ps):
    cls = [1 << i for i in range(m)]
    for p in ps:
        for b in p[0]:
            merged = b; rest = []
            for c in cls:
                if c & b: merged |= c
                else: rest.append(c)
            rest.append(merged); cls = rest
    return cls
def meet(C1, C2): return [x & y for x in C1 for y in C2 if x & y]
def finer(C1, C2): return all(any(x & K == x for K in C2) for x in C1)
t0 = time.time()
stats = {n: [0, 0, 0] for n in range(1, nmax + 1)}   # instances, failures(<=), failures(=)
pairs = [(a, c) for a in P for c in P if matched(a, c)]
if mode != 'all': random.seed(1); random.shuffle(pairs)
for a, c in pairs:
    if mode != 'all' and time.time() - t0 > float(sys.argv[4]): break
    idf = [x for x in P if theta(x, a) == theta(x, c)]
    layer = [c]
    for n in range(1, nmax + 1):
        layer = list({y for x in layer for y in idf if commute(x, y)})
        for xn in layer:
            for b in P:
                if not commute(xn, b): continue
                stats[n][0] += 1
                L = meet(classes(a, b), classes(b, c, xn)); R = classes(b, c)
                if not finer(L, R):
                    stats[n][1] += 1
                    print(f'  (T_{n}) <= FAILS: a={show(a,m)} c={show(c,m)} x_n={show(xn,m)} b={show(b,m)}', flush=True)
                if not finer(R, L): stats[n][2] += 1
for n in stats: print(f'P_{m} (T_{n}): {stats[n][0]} instances, {stats[n][1]} failures of <=, {stats[n][2]} failures of >= (i.e. of G1)')
print(f'{time.time()-t0:.0f}s')
