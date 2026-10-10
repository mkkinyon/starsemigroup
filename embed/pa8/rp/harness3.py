import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    Y = frozenset(range(n)) - s.sy
    for (Ai, Ci, Bi, G, Dl) in s.match:
        D = next(D for D in s.rho if Ai <= D)
        check('S10: Delta_i ∩ supp y ⊆ Gamma_i', (Dl & s.sy) <= G, fails, ex, s)
        check('S11: Gamma_i ∩ supp y ⊆ Delta_i', (G & s.sy) <= Dl, fails, ex, s)
        check('S12: Delta_i ∩ supp x ⊆ Gamma_i', (Dl & s.sx) <= G, fails, ex, s)
        check('S13: rho-class(A_i) ⊆ Gamma_i ∪ Delta_i', D <= (G | Dl), fails, ex, s)
        check('S14: rho-class(A_i) ∩ supp y ⊆ Gamma_i ∪ Delta_i', (D & s.sy) <= (G | Dl), fails, ex, s)
        check('S15: rho-class(A_i) ∩ supp y ⊆ Gamma_i', (D & s.sy) <= G, fails, ex, s)
        check('S16: rho-class(A_i) ∩ supp y ⊆ Delta_i', (D & s.sy) <= Dl, fails, ex, s)
        check('S17: Gamma_i ∩ supp x ⊆ Delta_i', (G & s.sx) <= Dl, fails, ex, s)
        check('S18: B_i ∩ supp y ⊆ Gamma_i', (Bi & s.sy) <= G, fails, ex, s)
        check('S19: A_i ∩ supp y ⊆ Delta_i', (Ai & s.sy) <= Dl, fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness3_ex.pkl', 'wb'))
