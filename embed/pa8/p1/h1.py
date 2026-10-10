import pickle, numpy as np, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
R = np.concatenate([pickle.load(open(f, 'rb')) for f in sys.argv[2:]])
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
fails = {}; ex = {}
def check(name, cond, s):
    if not cond:
        fails[name] = fails.get(name, 0) + 1; ex.setdefault(name, s)
for row in R:
    a, c, b, d, x = [P[i] for i in row]
    if len({row[0], row[1], row[2], row[3]}) < 4: continue
    Tb = lambda p: [t for t, tr in top_blocks(p, n) if tr]; Nb = lambda p: [t for t, tr in top_blocks(p, n) if not tr]
    A, C, B, D = Tb(a), Tb(c), Tb(b), Tb(d); sx = supp(x, n); sa, sc, sb, sd = supp(a, n), supp(c, n), supp(b, n), supp(d, n)
    Y = frozenset(range(n)) - sx
    Gam = join_classes([a, c], n); Del = join_classes([c, b], n); Lam = join_classes([b, d], n); rho = join_classes([a, d], n)
    kx_a = join_classes([x, a], n); kx_c = join_classes([x, c], n)
    U = [K for K in kx_a if K & sx and K & sa]; V = [K for K in kx_c if K & sx and K & sc]
    s = (a, c, b, d, x)
    match = []
    for Ai in A:
        G = next(G for G in Gam if Ai <= G); Ci = next(Cj for Cj in C if Cj <= G)
        Dl = next(K for K in Del if Ci <= K); Bi = next(Bj for Bj in B if Bj <= Dl)
        L = next(K for K in Lam if Bi <= K); Di = next(Dj for Dj in D if Dj <= L)
        match.append((Ai, Ci, Bi, Di, G, Dl, L))
    for (Ai, Ci, Bi, Di, G, Dl, L) in match:
        check('B_i ∩ supp x inside one U (or empty)', sum(1 for Ul in U if Bi & Ul) <= 1 and (Bi & sx) <= (frozenset().union(*U) if U else frozenset()), s)
        check('D_i ∩ supp x inside one V (or empty)', sum(1 for Vk in V if Di & Vk) <= 1 and (Di & sx) <= (frozenset().union(*V) if V else frozenset()), s)
        check('A_i and B_i in same U-class or both outside supp x', (not (Ai & sx) and not (Bi & sx)) or any((Ai & Ul) and (Bi & Ul) for Ul in U), s)
        check('C_i and D_i in same V or both outside', (not (Ci & sx) and not (Di & sx)) or any((Ci & Vk) and (Di & Vk) for Vk in V), s)
        check('rho-class of A_i contains D_i', Di <= next(K for K in rho if Ai <= K), s)
        check('Lambda_i ∩ supp x ⊆ ? (D_i)', (L & sx) <= Di, s)
        check('Delta_i ∩ supp x ⊆ C_i ∪ B_i', (Dl & sx) <= (Ci | Bi), s)
        check('Gamma_i ∩ supp x ⊆ A_i ∪ C_i', (G & sx) <= (Ai | Ci), s)
        check('Lambda_i ∩ supp x ⊆ B_i ∪ D_i', (L & sx) <= (Bi | Di), s)
    for N in Nb(c):
        if N <= sx: check('N(c) in supp x not in any Delta_i', not any(N <= Dl for (_,_,_,_,_,Dl,_) in match), s)
        if N <= sx: check('N(c) in supp x not in any Lambda_i', not any(N <= L for (_,_,_,_,_,_,L) in match), s)
    for N in Nb(a):
        if N <= sx: check('N(a) in supp x not in any Delta_i', not any(N <= Dl for (_,_,_,_,_,Dl,_) in match), s)
        if N <= sx: check('N(a) in supp x not in any Gamma_i', not any(N <= G for (_,_,_,_,G,_,_) in match), s)
    for N in Nb(b):
        if N <= sx: check('N(b) in supp x not in any Lambda_i', not any(N <= L for (_,_,_,_,_,_,L) in match), s)
        if N <= sx: check('N(b) in supp x not in any Delta_i', not any(N <= Dl for (_,_,_,_,_,Dl,_) in match), s)
    for N in Nb(d):
        if N <= sx: check('N(d) in supp x not in any Lambda_i', not any(N <= L for (_,_,_,_,_,_,L) in match), s)
print("instances (distinct path):", sum(1 for row in R if len(set(row[:4])) == 4))
for k, v in sorted(fails.items()): print(f"{v:5d} fail: {k}")
pickle.dump(ex, open('h1_ex.pkl', 'wb'))
