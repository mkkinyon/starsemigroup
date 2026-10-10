import sys, pickle
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y); count += 1
    DeltaB = [Dl for (_, _, _, _, Dl) in s.match]
    DeltaB = list({D: 1 for D in DeltaB})
    Dfree = [D for D in s.Delta if D not in DeltaB]
    for N in s.Na:
        if N <= s.sy:
            check('S20a: N(a)-block in supp y meets ≤1 Delta_i', sum(1 for D in DeltaB if N & D) <= 1, fails, ex, s)
            check('S20b: N(a)-block in supp y meets ≤1 Delta-class', sum(1 for D in s.Delta if N & D) <= 1, fails, ex, s)
            check('S20c: N(a)-block in supp y meeting a Delta_i meets no B-free Delta', not (any(N & D for D in DeltaB) and any(N & D for D in Dfree)), fails, ex, s)
    # symmetric: N(b)-blocks and Gamma
    GammaA = list({G: 1 for (_, _, _, G, _) in s.match})
    for N in s.Nb:
        if N <= s.sy:
            check('S20d: N(b)-block in supp y meets ≤1 Gamma_i', sum(1 for G in GammaA if N & G) <= 1, fails, ex, s)
    # A_i meets only Delta_i and B-free classes
    for (Ai, Ci, Bi, G, Dl) in s.match:
        check('S21: A_i meets no Delta_j (j≠i)', not any(Ai & D for D in DeltaB if D != Dl), fails, ex, s)
        check('S21b: B_i meets no Gamma_j (j≠i)', not any(Bi & G2 for G2 in GammaA if G2 != G), fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness4_ex.pkl', 'wb'))
