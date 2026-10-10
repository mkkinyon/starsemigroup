"""Embed a projection algebra (P, theta) into the projection algebra of P_n."""
import sys, time, itertools
from pmon import Pn, projections, rank
from embed import orbit_reps

def proj_algebra(T, star):
    n = len(T)
    P = [x for x in range(n) if star[x] == x and T[x][x] == x]
    loc = {p: i for i, p in enumerate(P)}
    th = [[loc[T[T[p][q]][p]] for q in P] for p in P]   # th[p][q] = p q p
    return th

def find_pa_embedding(th, n, limit=1):
    m = len(th); P = Pn(n); projs = projections(n)
    # order: elements by number of distinct theta-images (heuristic)
    order = sorted(range(m), key=lambda p: -len(set(th[p])))
    img = {}; used = set(); sols = []
    def consistent(x, v):
        for y, w in img.items():
            for (a, b, av, bv) in ((x, y, v, w), (y, x, w, v)):
                c = th[a][b]; val = P.prod(av, bv, av)
                if c in img:
                    if img[c] != val: return False
                elif c == x:
                    if val != v: return False
                elif c == y:
                    if val != w: return False
        if P.prod(v, v, v) != v: return False
        # pairs (a,b) already assigned with th[a][b] == x
        img2 = dict(img); img2[x] = v
        for a, va in img2.items():
            for b, vb in img2.items():
                c = th[a][b]
                if c in img2 and P.prod(va, vb, va) != img2[c]: return False
        return True
    reps = orbit_reps(type('D', (), {'n': n, 'projs': projs})())
    def rec(i, first):
        if sols: return
        if i == m: sols.append(dict(img)); return
        x = order[i]
        for v in (reps if first else projs):
            if v in used or not consistent(x, v): continue
            img[x] = v; used.add(v); rec(i + 1, False); del img[x]; used.discard(v)
            if sols: return
    rec(0, True)
    return sols

if __name__ == "__main__":
    from qsub4 import gen_sub, a0, a1, a2, b0, b1, b2
    Ts, ss, S = gen_sub([a0,a1,a2,b0,b1,b2])
    th = proj_algebra(Ts, ss)
    print("projection algebra size", len(th))
    for n in range(2, int(sys.argv[1]) + 1):
        t = time.time(); sols = find_pa_embedding(th, n)
        print(f"P(Q0) -> P(P_{n}): {'yes' if sols else 'no'} ({time.time()-t:.0f}s)", flush=True)
        if sols: break
