"""Embed small projection algebras (Mace4 models, table T[x][y] = y x y) into the projection algebra
P(P_m) of the partition monoid, m = 1..M, with forced propagation (the image of a product of assigned
elements is forced).  Usage: python3 pa_embed2.py pa_5.out [M]
Reports, for each model, the least m with an embedding, or NONE (up to M)."""
import sys, time, itertools, pickle
from pmon import projections, mul
from mace4parse import parse_models

class PPm:
    def __init__(self, m):
        self.m = m; self.projs = projections(m); self.idx = {p: i for i, p in enumerate(self.projs)}
        N = len(self.projs); self.N = N
        t = time.time()
        self.tab = [[0] * N for _ in range(N)]     # tab[x][y] = y x y
        for y, q in enumerate(self.projs):
            for x, p in enumerate(self.projs):
                self.tab[x][y] = self.idx[mul(mul(q, p, m), q, m)]
        seen = set(); self.reps = []
        for i, p in enumerate(self.projs):
            if i in seen: continue
            self.reps.append(i)
            for perm in itertools.permutations(range(m)):
                q = tuple(sorted(tuple(sorted(perm[x] if x < m else m + perm[x - m] for x in blk)) for blk in p))
                seen.add(self.idx[q])
        self.time = time.time() - t

def embed(T, D, limit=None, all_first=False):
    """injective img with img[T[x][y]] = tab[img[x]][img[y]]; returns img, None, or 'timeout'."""
    k = len(T); tab = D.tab; N = D.N
    img = [-1] * k; used = set(); t0 = time.time()
    def forced():
        for x in range(k):
            if img[x] < 0: continue
            for y in range(k):
                if img[y] < 0: continue
                z = T[x][y]
                if img[z] < 0: return z, tab[img[x]][img[y]]
        return None
    def consistent():
        for x in range(k):
            if img[x] < 0: continue
            for y in range(k):
                if img[y] < 0: continue
                z = img[T[x][y]]
                if z >= 0 and z != tab[img[x]][img[y]]: return False
        return True
    def rec(depth):
        if limit and time.time() - t0 > limit: raise TimeoutError
        if all(v >= 0 for v in img): return True
        f = forced()
        if f is not None:
            z, v = f
            if v in used: return False
            img[z] = v; used.add(v)
            ok = consistent() and rec(depth + 1)
            if ok: return True
            img[z] = -1; used.discard(v)
            return False
        x = max((i for i in range(k) if img[i] < 0), key=lambda i: len(set(T[i]) | {T[j][i] for j in range(k)}))
        cands = D.reps if (depth == 0 and not all_first) else range(N)
        for v in cands:
            if v in used: continue
            img[x] = v; used.add(v)
            if consistent() and rec(depth + 1): return True
            img[x] = -1; used.discard(v)
        return False
    try:
        ok = rec(0)
    except TimeoutError:
        return "timeout"
    return list(img) if ok else None

if __name__ == "__main__":
    fname = sys.argv[1]; M = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    models = list(parse_models(open(fname).read()))
    print(f"{len(models)} models in {fname}", flush=True)
    Ds = {}; results = []
    for mi, (N, T, consts) in enumerate(models):
        found = None
        for m in range(1, M + 1):
            if m not in Ds:
                Ds[m] = PPm(m); print(f"  P(P_{m}): {Ds[m].N} projections, {len(Ds[m].reps)} orbits ({Ds[m].time:.0f}s)", flush=True)
            r = embed(T, Ds[m], limit=1200)
            if r == "timeout": print(f"model {mi}: timeout at m={m}", flush=True); continue
            if r is not None: found = (m, r); break
        results.append((N, T, found))
        print(f"model {mi} (order {N}): {'embeds in P(P_%d)' % found[0] if found else 'NO embedding up to P(P_%d)' % M}", flush=True)
    with open(fname.replace(".out", "_embed.pkl"), "wb") as f: pickle.dump(results, f)
    from collections import Counter
    print("summary:", Counter(f[0] if f else None for _, _, f in results))
