"""Structural harness for (Q) instances: path a|><|c|><|b|><|d, u<=a with th_c(u)=th_d(u), y~a, y~b, th_y(c)=th_y(b)."""
import sys, pickle, itertools
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks, join_classes
class S: pass
def blocks(p, n):
    tb = [t for t, tr in top_blocks(p, n) if tr]; nbk = [t for t, tr in top_blocks(p, n) if not tr]
    sp = frozenset().union(*tb) if tb else frozenset()
    return tb, nbk, sp
def cls(K, classes): return next(L for L in classes if K <= L)
def structure(P, n, a, c, b, d, u, y):
    s = S(); s.n = n
    s.A, s.Na, s.sa = blocks(P[a], n); s.C, s.Nc, s.sc = blocks(P[c], n); s.B, s.Nb, s.sb = blocks(P[b], n); s.D, s.Nd, s.sd = blocks(P[d], n)
    s.U, s.Nu, s.su = blocks(P[u], n); s.Y, s.Ny, s.sy = blocks(P[y], n)
    s.Gamma = join_classes([P[a], P[c]], n); s.Delta = join_classes([P[c], P[b]], n); s.Lam = join_classes([P[b], P[d]], n)
    s.rho = join_classes([P[a], P[d]], n); s.Pi1 = join_classes([P[u], P[c]], n); s.Pi1d = join_classes([P[u], P[d]], n)
    s.cd = join_classes([P[c], P[d]], n)
    s.Pa = join_classes([P[y], P[a]], n); s.Pb = join_classes([P[y], P[b]], n); s.Kc = join_classes([P[y], P[c]], n); s.Kd = join_classes([P[y], P[d]], n)
    s.match = []   # (A_i, C_i, B_i, D_i)
    for Ai in s.A:
        Ci = next(Cj for Cj in s.C if Cj <= cls(Ai, s.Gamma)); Bi = next(Bj for Bj in s.B if Bj <= cls(Ci, s.Delta)); Di = next(Dj for Dj in s.D if Dj <= cls(Bi, s.Lam))
        s.match.append((Ai, Ci, Bi, Di))
    # groups of u: u-blocks inside supp a, with labels
    s.groups = []   # (frozenset of indices i, label T/F, A_G, C_G)
    for blk, lab in [(t, True) for t in s.U] + [(t, False) for t in s.Nu]:
        if blk <= s.sa:
            idx = frozenset(i for i, (Ai, _, _, _) in enumerate(s.match) if Ai <= blk)
            assert frozenset().union(*[s.match[i][0] for i in idx]) == blk
            s.groups.append((idx, lab, blk, frozenset().union(*[s.match[i][1] for i in idx])))
    return s
def show(P, n, i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
def run(n, files, claims, maxshow=2):
    P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
    fails = {}; ex = {}; count = 0
    for f in files:
        for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
            if len({a, c, b, d}) < 4: continue
            for u in us:
                for y in ys:
                    s = structure(P, n, a, c, b, d, u, y); s.ids = (a, c, b, d, u, y); count += 1
                    for name, fn in claims.items():
                        try: ok = fn(s)
                        except Exception as e: ok = False; name = name + ' [EXC ' + repr(e)[:40] + ']'
                        if not ok:
                            fails[name] = fails.get(name, 0) + 1
                            if name not in ex: ex[name] = s
    print(f"P_{n}: {count} instances")
    for name in claims:
        print(f"  {name:70s} fails {fails.get(name, 0)}")
    for name, s in list(ex.items())[:maxshow]:
        print("  example for", name)
        for nm, i in zip('acbduy', s.ids): print(f"    {nm} = {show(P, n, i)}")
    return fails, ex
