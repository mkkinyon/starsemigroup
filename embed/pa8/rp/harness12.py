import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    for (Ai, Ci, Bi, G, Dl) in s.match:
        if Ai <= s.sy: continue
        M = next(N for N in s.Ny if Ai <= N)
        KM = next(K for K in s.sigma if M <= K)
        check('S48: i∉I: Delta_i ⊆ sigma-class of M', Dl <= KM, fails, ex, s)
        check('S51: i∉I: sigma-class of M misses supp y', not (KM & s.sy), fails, ex, s)
        check('S52: i∉I: sigma-class of M misses supp x', not (KM & s.sx), fails, ex, s)
        check('S53: i∉I: Delta_i misses supp x', not (Dl & s.sx), fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness12_ex.pkl', 'wb'))
