import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    for N in s.Nc:
        if N <= s.sx:
            check('S38: N(c)-block in supp x inside one N(a)-block', any(N <= Na for Na in s.Na), fails, ex, s)
            DeltaB = [Dl for (_, _, _, _, Dl) in s.match]
            if any(N <= D for D in DeltaB):
                check('S38b: N(c)-block in supp x lying in some Delta_i is inside one N(a)-block', any(N <= Na for Na in s.Na), fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness10_ex.pkl', 'wb'))
