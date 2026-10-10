"""Search P_n for six projections satisfying the length<=L relations of a0,a1,a2,b0,b1,b2 in Q_0."""
import sys, time, itertools
from pmon import Pn, projections, rank
from qsub4 import Tq, sq, a0, a1, a2, b0, b1, b2
from embed import orbit_reps

G = [a0, a1, a2, b0, b1, b2]; names = ['a0','a1','a2','b0','b1','b2']

def word_val_Q(w):
    r = G[w[0]]
    for i in w[1:]: r = Tq[r][G[i]]
    return r

def relations(L, letters):
    """pairs of words over `letters` (indices) of length <= L that are equal in Q_0, and
    words that are equal to a single letter."""
    ws = [w for l in range(1, L + 1) for w in itertools.product(letters, repeat=l)]
    val = {w: word_val_Q(w) for w in ws}
    groups = {}
    for w in ws: groups.setdefault(val[w], []).append(w)
    eq = [g for g in groups.values() if len(g) > 1]
    return ws, val, eq

def search(n, L=3):
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    def val_P(w, img):
        r = img[w[0]]
        for i in w[1:]: r = P.mul(r, img[i])
        return r
    # relations restricted to letters assigned so far
    order = [0, 3, 1, 4, 2, 5]   # a0, b0, a1, b1, a2, b2
    rel_cache = {}
    def rels(k):
        letters = order[:k]
        if k not in rel_cache:
            rel_cache[k] = relations(L, letters)
        return rel_cache[k]
    def check(img, k):
        ws, val, eq = rels(k)
        vp = {w: val_P(w, img) for w in ws}
        rep = {}
        for w in ws:
            q = val[w]; p = vp[w]
            if q in rep:
                if rep[q] != p: return False
            else: rep[q] = p
        return len(set(rep.values())) == len(rep)
    sols = []
    def rec(k, img):
        if sols: return
        if k == 6:
            sols.append(dict(img)); return
        x = order[k]
        cands = reps if k == 0 else projs
        for v in cands:
            if v in img.values(): continue
            img[x] = v
            if check(img, k + 1):
                rec(k + 1, img)
            del img[x]
            if sols: return
    rec(0, {})
    return sols

if __name__ == "__main__":
    L = int(sys.argv[2])
    for n in range(2, int(sys.argv[1]) + 1):
        t = time.time(); s = search(n, L)
        print(f"n={n}, L={L}: {'FOUND' if s else 'none'} ({time.time()-t:.0f}s)", flush=True)
        if s:
            for i, nm in enumerate(names): print("  ", nm, s[0][i])
            break
