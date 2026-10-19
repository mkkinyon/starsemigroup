"""Independent verification of the (Q)-violating 1-periodic configuration in P_N found by hotel_sat.
Points (i,j), i>=0, j in {0,1,2,3}. Window of M indices; theta computed by partition multiplication;
blocks are compared away from the window end."""
import sys
M = int(sys.argv[1]) if len(sys.argv) > 1 else 40
pts = [(i, j) for i in range(M) for j in range(4)]
def P(T, N):
    T = [frozenset(b) for b in T]; N = [frozenset(b) for b in N]
    cov = set().union(*T, *N)
    N = N + [frozenset([p]) for p in pts if p not in cov]           # remaining points: N-singletons
    blocks = [frozenset((p, s) for p in b for s in (0, 1)) for b in T]
    for b in N:
        blocks.append(frozenset((p, 0) for p in b)); blocks.append(frozenset((p, 1) for p in b))
    assert sum(len(b) for b in T) + sum(len(b) for b in N) == len(pts)
    return frozenset(blocks)
R = range(1, M)
a = P([[(0,0),(0,3)], [(0,1)], [(0,2)]] + [[(i,0)] for i in R] + [[(i,2)] for i in R],
      [[(i,3),(i+1,1)] for i in R if i+1 < M])
b = P([[(0,1)]] + [[(i,1)] for i in R] + [[(i,3)] for i in R],
      [[(0,0),(0,3)]] + [[(i,2),(i+1,0)] for i in range(M) if i+1 < M])
c = P([[(0,1)], [(0,2)], [(0,3),(1,1)]] + [[(i,2)] for i in R] + [[(i,1)] for i in range(2, M)],
      [[(i,0),(i,3)] for i in R])
d = P([[(i,0)] for i in range(M)] + [[(i,3)] for i in R],
      [[(0,1),(0,2)], [(0,3),(1,1)]] + [[(i,2),(i+1,1)] for i in R if i+1 < M])
x = P([], [[(0,0),(0,3)], [(0,1),(0,2)]] + [[(i,0),(i,2)] for i in R] + [[(i,3),(i+1,1)] for i in R if i+1 < M])
y = P([[(i,1)] for i in R] + [[(i,3)] for i in R],
      [[(0,0),(0,3)]] + [[(i,2),(i+1,0)] for i in range(M) if i+1 < M])
def mult(Pa, Pb):
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: u = par[u]
        return u
    def un(p, q): par[f(p)] = f(q)
    for bl in Pa:
        l = [('u', p) if s == 0 else ('m', p) for (p, s) in bl]
        for q in l[1:]: un(l[0], q)
    for bl in Pb:
        l = [('m', p) if s == 0 else ('l', p) for (p, s) in bl]
        for q in l[1:]: un(l[0], q)
    cls = {}
    for p in pts:
        cls.setdefault(f(('u', p)), set()).add((p, 0)); cls.setdefault(f(('l', p)), set()).add((p, 1))
    return frozenset(frozenset(v) for v in cls.values())
def th(p, q): return mult(mult(p, q), p)
def far(bl, margin): return any(p[0] >= M - margin for (p, s) in bl)
def same(Pp, Qq, margin=6):
    return [sorted(bl) for bl in Pp ^ Qq if not far(bl, margin)]
def show(name, diff): print(f"{name}: {'OK' if not diff else diff[:3]}")
show("a|><|c: theta_c(a)=c", same(th(c,a), c)); show("          theta_a(c)=a", same(th(a,c), a))
show("c|><|b: theta_b(c)=b", same(th(b,c), b)); show("          theta_c(b)=c", same(th(c,b), c))
show("b|><|d: theta_d(b)=d", same(th(d,b), d)); show("          theta_b(d)=b", same(th(b,d), b))
show("x~a: theta_x(a)=theta_a(x)", same(th(x,a), th(a,x)))
show("theta_c(x)=theta_d(x)", same(th(c,x), th(d,x)))
show("y~a", same(th(y,a), th(a,y))); show("y~b", same(th(y,b), th(b,y)))
show("theta_y(c)=theta_y(b)", same(th(y,c), th(y,b)))
print("a|><|d fails: theta_a(d) vs a, differing blocks near the start:", sorted(same(th(a,d), a))[:4])
print("                theta_d(a) vs d:", sorted(same(th(d,a), d))[:4])
# join classes of eps_a v eps_d: span check and T-block content
def classes(Pp, Qq):
    par = {}
    def f(u):
        while par.setdefault(u, u) != u: u = par[u]
        return u
    for bl in list(Pp) + list(Qq):
        l = [p for (p, s) in bl if s == 0]
        for q in l[1:]: par[f(l[0])] = f(q)
    cls = {}
    for p in pts: cls.setdefault(f(p), []).append(p)
    return list(cls.values())
def Tblocks(Pp): return [frozenset(p for (p, s) in bl if s == 0) for bl in Pp if any(s == 1 for (p, s) in bl) and any(s == 0 for (p, s) in bl)]
TA, TD = Tblocks(a), Tblocks(d)
spans = []
for K in sorted(classes(a, d))[:8]:
    Ks = set(K); As = [sorted(B) for B in TA if B <= Ks]; Ds = [sorted(B) for B in TD if B <= Ks]
    print("class", sorted(K), " T(a):", As, " T(d):", Ds)
print("max span of a join class (a,d), (a,c), (c,b), (b,d), (x,c), (x,d), (y,c), (y,b):",
      [max(max(i for (i,j) in K) - min(i for (i,j) in K) for K in classes(p, q)) for (p, q) in [(a,d),(a,c),(c,b),(b,d),(x,c),(x,d),(y,c),(y,b)]])
