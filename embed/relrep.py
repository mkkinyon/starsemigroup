"""Search for representations of a finite regular *-semigroup by binary relations on a set Y
with converse as involution (Schein-type representations)."""
import sys, itertools, pickle, time
from embed import semigroup_data

def rel_tools(m):
    N = m * m
    def comp(R, S):
        out = 0
        for i in range(m):
            row = (R >> (i * m)) & ((1 << m) - 1)
            if row:
                acc = 0
                for j in range(m):
                    if row >> j & 1:
                        acc |= (S >> (j * m)) & ((1 << m) - 1)
                out |= acc << (i * m)
        return out
    def conv(R):
        out = 0
        for i in range(m):
            for j in range(m):
                if R >> (i * m + j) & 1:
                    out |= 1 << (j * m + i)
        return out
    return comp, conv

def find_relrep(T, star, m, limit=1):
    n = len(T)
    comp, conv = rel_tools(m)
    allrel = range(1 << (m * m))
    pers = [R for R in allrel if conv(R) == R and comp(R, R) == R]
    P, below = semigroup_data(T, star)
    others = [x for x in range(n) if x not in P]
    order = P + others
    sols = []
    cache = {}
    def hcands(a, b):
        key = (a, b)
        if key not in cache:
            cache[key] = [R for R in allrel if comp(R, conv(R)) == a and comp(conv(R), R) == b]
        return cache[key]
    def close(img):
        img = dict(img); used = {}
        for x, v in img.items():
            if v in used: return None
            used[v] = x
        changed = True
        while changed:
            changed = False
            items = list(img.items())
            for a, va in items:
                sa = star[a]
                if sa not in img:
                    w = conv(va)
                    if w in used: return None
                    img[sa] = w; used[w] = sa; changed = True
                for b, vb in items:
                    c = T[a][b]; w = comp(va, vb)
                    if c in img:
                        if img[c] != w: return None
                    else:
                        if w in used: return None
                        img[c] = w; used[w] = c; changed = True
        return img
    def rec(img):
        if len(sols) >= limit: return
        for x in order:
            if x not in img: break
        else:
            sols.append(img); return
        if x in P:
            cands = pers
        else:
            cands = hcands(img[T[x][star[x]]], img[T[star[x]][x]])
        used = set(img.values())
        for v in cands:
            if v in used: continue
            img2 = dict(img); img2[x] = v
            img2 = close(img2)
            if img2 is None: continue
            rec(img2)
            if len(sols) >= limit: return
    rec({})
    return sols

if __name__ == "__main__":
    from pmon import partition_monoid, mul, star as pstar
    n = 2
    elems = partition_monoid(n)
    idx = {e: i for i, e in enumerate(elems)}
    T = [[idx[mul(p, q, n)] for q in elems] for p in elems]
    st = [idx[pstar(p, n)] for p in elems]
    for m in range(1, 5):
        t = time.time()
        sols = find_relrep(T, st, m)
        print(f"P_2 -> relations on {m} points: {'yes' if sols else 'no'} ({time.time()-t:.1f}s)", flush=True)
        if sols: break
