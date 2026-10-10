"""Structural test harness on reduced (x<=y) (R') instances of P_n."""
import sys, pickle
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '.')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
inst = pickle.load(open(sys.argv[2] if len(sys.argv) > 2 else f'inst{n}.pkl', 'rb'))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
class S: pass
def structure(a, c, b, x, y):
    s = S(); s.a, s.c, s.b, s.x, s.y = a, c, b, x, y
    s.A = [t for t, tr in top_blocks(a, n) if tr]; s.Na = [t for t, tr in top_blocks(a, n) if not tr]
    s.C = [t for t, tr in top_blocks(c, n) if tr]; s.Nc = [t for t, tr in top_blocks(c, n) if not tr]
    s.B = [t for t, tr in top_blocks(b, n) if tr]; s.Nb = [t for t, tr in top_blocks(b, n) if not tr]
    s.H = [t for t, tr in top_blocks(y, n) if tr]; s.Ny = [t for t, tr in top_blocks(y, n) if not tr]
    s.Hx = [t for t, tr in top_blocks(x, n) if tr]; s.Nx = [t for t, tr in top_blocks(x, n) if not tr]
    s.sa, s.sb, s.sc, s.sx, s.sy = supp(a, n), supp(b, n), supp(c, n), supp(x, n), supp(y, n)
    s.Gamma = join_classes([a, c], n); s.Delta = join_classes([b, c], n); s.rho = join_classes([a, b], n)
    s.kappa = join_classes([y, a], n); s.tau = join_classes([y, c], n); s.sigma = join_classes([y, b], n)
    s.U = [K for K in s.kappa if K & s.sy and K & s.sa]; s.V = [K for K in s.tau if K & s.sy and K & s.sc]
    # matching A_i -> C_i -> B_i
    s.match = []
    for Ai in s.A:
        G = next(D for D in s.Gamma if Ai <= D); Ci = next(Cj for Cj in s.C if Cj <= G)
        Dl = next(D for D in s.Delta if Ci <= D); Bi = next(Bj for Bj in s.B if Bj <= Dl)
        s.match.append((Ai, Ci, Bi, G, Dl))
    r = th(x, b); s.r = r
    s.R = [t for t, tr in top_blocks(r, n)]; s.RT = [t for t, tr in top_blocks(r, n) if tr]
    s.Ntil = [N for N in s.Nc if N <= s.sy and not (N <= s.sx)]  # N(c)-blocks in supp y \ supp x
    return s
def check(name, cond, fails, ex, s):
    if not cond:
        fails[name] = fails.get(name, 0) + 1
        if name not in ex: ex[name] = s
fails = {}; ex = {}; count = 0
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)  # reduce: x <= y
    s = structure(a, c, b, x, y); count += 1
    I = [(Ai, Ci, Bi, G, Dl) for (Ai, Ci, Bi, G, Dl) in s.match if Ai <= s.sy]
    notI = [t for t in s.match if not (t[0] <= s.sy)]
    # S4a: Delta_i meets supp y only inside the V containing C_i (i in I); for i not in I, Delta_i misses supp y
    for (Ai, Ci, Bi, G, Dl) in I:
        Vk = next(V for V in s.V if Ci <= V)
        check('S4a: Delta_i ∩ supp y ⊆ V_k(i)', (Dl & s.sy) <= Vk, fails, ex, s)
        check('S4c: Delta_i ∩ supp y ⊆ C_i', (Dl & s.sy) <= Ci, fails, ex, s)
        check('S4d: Delta_i ∩ supp x ⊆ C_i', (Dl & s.sx) <= Ci, fails, ex, s)
    for (Ai, Ci, Bi, G, Dl) in notI:
        check('S4b: Delta_i (i∉I) ∩ supp y = ∅', not (Dl & s.sy), fails, ex, s)
        check('S4e: Delta_i (i∉I) ∩ supp x = ∅', not (Dl & s.sx), fails, ex, s)
        D = next(D for D in s.rho if Ai <= D)
        check('S5: rho-class of A_i (i∉I) has T-blocks A_i,B_i only', [Aj for Aj in s.A if Aj <= D] == [Ai] and [Bj for Bj in s.B if Bj <= D] == [Bi], fails, ex, s)
    # Ntil not in any Delta_i
    for N in s.Ntil:
        check('S4f: Ntil not in Delta_i', not any(N <= Dl for (_, _, _, _, Dl) in s.match), fails, ex, s)
    # every V_k meets supp r; r-blocks meeting V_k lie in V_k
    sr = supp(s.r, n)
    for V in s.V:
        check('F4a: V_k meets supp r', bool(V & sr), fails, ex, s)
        for R in s.R:
            if R & V: check('F4b: r-block meeting V_k inside V_k', R <= V, fails, ex, s)
    for U in s.U:
        check('F4c: U_l meets supp r', bool(U & sr), fails, ex, s)
        for R in s.R:
            if R & U: check('F4d: r-block meeting U_l inside U_l', R <= U, fails, ex, s)
    # B_i inside supp y? B_i ∩ supp y ⊆ V_k(i)?
    for (Ai, Ci, Bi, G, Dl) in I:
        Vk = next(V for V in s.V if Ci <= V)
        check('S8: B_i ∩ supp y ⊆ V_k(i)', (Bi & s.sy) <= Vk, fails, ex, s)
        check('S9: B_i ∩ supp y ⊆ C_i', (Bi & s.sy) <= Ci, fails, ex, s)
print("instances (a!=c):", count)
for k, v in sorted(fails.items()): print(f"{v:6d} fail: {k}")
pickle.dump({k: (s.a, s.c, s.b, s.x, s.y) for k, s in ex.items()}, open('harness_ex.pkl', 'wb'))
