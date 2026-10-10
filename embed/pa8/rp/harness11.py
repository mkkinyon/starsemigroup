import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    for (Ai, Ci, Bi, G, Dl) in s.match:
        if Ai <= s.sy: continue
        D = next(D for D in s.rho if Ai <= D)
        for N in s.Nc:
            if N <= s.sx and N <= Dl:
                check('S44: i∉I, N(c)-block in supp x in Delta_i is inside one N(a)-block', any(N <= Na for Na in s.Na), fails, ex, s)
                check('S44b: ... and that N(a)-block is in rho-class of A_i', any(N <= Na and Na <= D for Na in s.Na), fails, ex, s)
        for Z in [t for t, tr in top_blocks(b, n)]:
            if Z <= Dl: check('S45: i∉I: every b-block of Delta_i is in rho-class of A_i', Z <= D, fails, ex, s)
        check('S46: i∉I: Delta_i ⊆ rho-class of A_i', Dl <= D, fails, ex, s)
        check('S47: i∉I: Delta_i ∩ supp x = ∅ or ...', True, fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness11_ex.pkl', 'wb'))
