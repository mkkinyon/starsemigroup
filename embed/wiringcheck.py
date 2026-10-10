"""Check the wiring conditions (S) and (S*) on a projection algebra given as table T[x][y] = y x y."""
import itertools
def check(T, name):
    N = len(T); op = lambda x, y: T[x][y]   # op(x,y) = theta_y(x)
    th = lambda p, q: T[q][p]               # theta_p(q)
    bad_S = bad_T = 0; ex = None
    for a, b, c, d in itertools.product(range(N), repeat=4):
        if not (th(a,c)==a and th(c,a)==c and th(b,c)==b and th(c,b)==c and th(b,d)==b and th(d,b)==d): continue
        z = th(c,d)
        if z != th(d,c): continue
        if th(a,z) != th(b,z): continue
        if not (th(a,d)==a and th(d,a)==d):
            bad_S += 1; ex = ex or (a,b,c,d)
            if th(a,d) == th(a,z) and a != b: bad_T += 1
    print(f"{name}: (S) violations {bad_S}, Theorem violations {bad_T}", ex)
if __name__ == "__main__":
    from qsub4 import gen_sub, a0, a1, a2, b0, b1, b2
    from pa_embed import proj_algebra
    Ts, ss, S = gen_sub([a0,a1,a2,b0,b1,b2]); th = proj_algebra(Ts, ss)
    T = [[th[y][x] for y in range(len(th))] for x in range(len(th))]   # th[p][q] = p q p ; T[x][y] = y x y
    check(T, "P(Q0)")
    from mace4parse import parse_models
    for f in ["mace_tri15.out", "mace_path14.out", "mace_square13.out", "mace_disjoint14.out"]:
        for N, T, c in parse_models(open(f).read()):
            check(T, f); break
