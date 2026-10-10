"""Search for *-embeddings of a finite regular *-semigroup (T, star) into P_n."""
import itertools, sys, pickle, time
from pmon import Pn, projections, rank

class PnData:
    def __init__(self, n):
        self.n = n
        self.P = Pn(n)
        self.projs = projections(n)
        self.rank = {p: rank(p, n) for p in self.projs}
        self._hclass = {}
    def hclass(self, a, b):
        """elements x of P_n with x x* = a, x* x = b (a, b projections of equal rank)."""
        key = (a, b)
        if key in self._hclass:
            return self._hclass[key]
        n = self.n
        At = [blk for blk in a if blk[0] < n and blk[-1] >= n]
        Bt = [blk for blk in b if blk[0] < n and blk[-1] >= n]
        Na = [blk for blk in a if blk[-1] < n]
        Nb = [blk for blk in b if blk[0] >= n]
        res = []
        if len(At) == len(Bt):
            Aup = [tuple(x for x in blk if x < n) for blk in At]
            Blo = [tuple(x for x in blk if x >= n) for blk in Bt]
            for perm in itertools.permutations(range(len(Bt))):
                blocks = [Aup[i] + Blo[perm[i]] for i in range(len(At))] + Na + Nb
                res.append(tuple(sorted(tuple(sorted(bl)) for bl in blocks)))
        self._hclass[key] = res
        return res

def semigroup_data(T, star):
    n = len(T)
    P = [x for x in range(n) if star[x] == x and T[x][x] == x]
    # J-order: x <=_J y iff x in S^1 y S^1
    below = [[False] * n for _ in range(n)]
    for y in range(n):
        ideal = {y}
        for a in range(n):
            ideal.add(T[a][y]); ideal.add(T[y][a])
            for b in range(n):
                ideal.add(T[T[a][y]][b])
        for x in ideal:
            below[x][y] = True
    return P, below

def orbit_reps(D):
    """one representative of each S_n-orbit on the projections of P_n"""
    n = D.n
    seen = set(); reps = []
    for p in D.projs:
        if p in seen:
            continue
        reps.append(p)
        for perm in itertools.permutations(range(n)):
            q = tuple(sorted(tuple(sorted(perm[x] if x < n else n + perm[x - n] for x in blk)) for blk in p))
            seen.add(q)
    return reps

def find_embedding(T, star, D, all_solutions=False, limit=1, use_symmetry=True):
    """D: PnData. Returns a list of embeddings (dict element -> partition).
    Images are chosen for one element at a time (projections first); the images of all
    products of assigned elements are forced and checked."""
    n = len(T)
    P, below = semigroup_data(T, star)
    # order: by J-class from the top (elements above many others first); projections before others
    height = [sum(1 for y in range(n) if below[y][x]) for x in range(n)]
    order = sorted(range(n), key=lambda x: (-height[x], x not in P, x))
    sols = []
    if not hasattr(D, "_reps"):
        D._reps = orbit_reps(D)

    def close(img):
        """extend img by forced images; return new img or None."""
        img = dict(img)
        used = {}
        for x, v in img.items():
            if v in used:
                return None
            used[v] = x
        changed = True
        while changed:
            changed = False
            items = list(img.items())
            for a, va in items:
                sa = star[a]
                if sa not in img:
                    w = D.P.star(va)
                    if w in used:
                        return None
                    img[sa] = w; used[w] = sa; changed = True
                for b, vb in items:
                    c = T[a][b]
                    w = D.P.mul(va, vb)
                    if c in img:
                        if img[c] != w:
                            return None
                    else:
                        if w in used:
                            return None
                        img[c] = w; used[w] = c; changed = True
        return img

    def rank_ok(img, x, v):
        k = D.rank[v]
        for y, w in img.items():
            if y in P:
                ky = D.rank[w]
                if below[x][y] and below[y][x] and k != ky:
                    return False
                if below[x][y] and not below[y][x] and k > ky:
                    return False
                if below[y][x] and not below[x][y] and k < ky:
                    return False
        return True

    def rec(img, first):
        if len(sols) >= limit and not all_solutions:
            return
        for x in order:
            if x not in img:
                break
        else:
            sols.append(img)
            return
        if x in P:
            cands = D._reps if (first and use_symmetry) else D.projs
        else:
            xx = T[x][star[x]]; xsx = T[star[x]][x]
            if xx not in img or xsx not in img:
                # assign the projections first
                x = xx if xx not in img else xsx
                cands = D._reps if (first and use_symmetry) else D.projs
            else:
                cands = D.hclass(img[xx], img[xsx])
        used = set(img.values())
        for v in cands:
            if v in used:
                continue
            if x in P and not rank_ok(img, x, v):
                continue
            img2 = dict(img); img2[x] = v
            img2 = close(img2)
            if img2 is None:
                continue
            rec(img2, False)
            if len(sols) >= limit and not all_solutions:
                return
    rec({}, True)
    return sols

def check_embedding(T, star, emb, D):
    n = len(T)
    for x in range(n):
        assert D.P.star(emb[x]) == emb[star[x]]
        for y in range(n):
            assert D.P.mul(emb[x], emb[y]) == emb[T[x][y]]
    assert len(set(emb.values())) == n

if __name__ == "__main__":
    fn = sys.argv[1]; nmax = int(sys.argv[2])
    allres = pickle.load(open(fn, "rb"))
    Ds = {n: PnData(n) for n in range(1, nmax + 1)}
    out = {}
    for order in sorted(allres):
        t = time.time()
        res = []
        for idx, (T, star) in enumerate(allres[order]):
            deg = None
            for n in range(1, nmax + 1):
                sols = find_embedding(T, star, Ds[n])
                if sols:
                    check_embedding(T, star, sols[0], Ds[n])
                    deg = n
                    break
            res.append(deg)
        out[order] = res
        cnt = {}
        for d in res:
            cnt[d] = cnt.get(d, 0) + 1
        print(f"order {order}: {len(res)} semigroups; min degree counts {dict(sorted(cnt.items(), key=lambda kv: (kv[0] is None, kv[0])))}  ({time.time()-t:.0f}s)", flush=True)
    with open(fn.replace(".pkl", f"_emb{nmax}.pkl"), "wb") as f:
        pickle.dump(out, f)
