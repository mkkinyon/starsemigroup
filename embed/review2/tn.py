"""Brute-force test of (T_1) and variants in P_m: a|><|c, c~x, theta_x(a)=theta_x(c), x~b  =>  (e_a v e_b) ^ (e_b v e_c v e_x) = e_b v e_c."""
import sys
from fast import *
m = int(sys.argv[1]); P = projections(m)
def classes(*ps):
    cls = [1 << i for i in range(m)]
    for p in ps:
        for b in p[0]:
            merged = b; rest = []
            for c in cls:
                if c & b: merged |= c
                else: rest.append(c)
            rest.append(merged); cls = rest
    return frozenset(cls)
def meet(C1, C2):
    return frozenset(x & y for x in C1 for y in C2 if x & y)
def leq(C1, C2):  # partition C1 finer than C2
    return all(any(x & K == x for K in C2) for x in C1)
cnt = 0; bad = 0; badT1b = 0; ex = None
for a in P:
    for c in P:
        if not matched(a, c): continue
        for x in P:
            if not commute(x, c) or theta(x, a) != theta(x, c): continue
            for b in P:
                if not commute(x, b): continue
                cnt += 1
                L = meet(classes(a, b), classes(b, c, x)); R = classes(b, c)
                if L != R:
                    bad += 1
                    if matched(b, c): badT1b += 1
                    if ex is None or sum(len(p[0]) for p in (a,c,x,b)) > sum(len(p[0]) for p in ex): ex = (a, c, x, b)
print(f'P_{m}: {cnt} instances of (T_1) hypotheses, {bad} failures ({badT1b} with b|><|c)')
if ex: print('example:', ' '.join(f'{n}={show(p,m)}' for n, p in zip('acxb', ex)))
