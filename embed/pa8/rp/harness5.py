import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    abc = join_classes([a, b, c], n)
    for K in abc:
        check('S24: class of a∨b∨c has ≤1 C', sum(1 for C in s.C if C <= K) <= 1, fails, ex, s)
    abcy = join_classes([a, b, c, y], n)
    for K in abcy:
        check('S25: class of a∨b∨c∨y has ≤1 C', sum(1 for C in s.C if C <= K) <= 1, fails, ex, s)
    abx = join_classes([a, b, x], n)
    for K in abx:
        check('S26: class of a∨b∨x has ≤1 A', sum(1 for A in s.A if A <= K) <= 1, fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness5_ex.pkl', 'wb'))
