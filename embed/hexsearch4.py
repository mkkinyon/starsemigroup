import sys, time, itertools
from pmon import Pn, projections
from hexsearch import relations, names, G, Tq
from embed import orbit_reps

def search_pair(n, pair, L=3, limit=1):
    """six projections (not nec. distinct) satisfying all equalities, with x_pair[0] != x_pair[1]."""
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    order = [0, 3, 1, 4, 2, 5]
    ws, val, eq = relations(L, list(range(6)))
    level_words = []
    for k in range(6):
        allowed = set(order[:k + 1]); new = order[k]
        level_words.append([w for w in ws if set(w) <= allowed and new in w])
    def val_P(w, img):
        r = img[w[0]]
        for i in w[1:]: r = P.mul(r, img[i])
        return r
    sols = []
    def rec(k, img, qp):
        if len(sols) >= limit: return
        if k == 6: sols.append(dict(img)); return
        x = order[k]
        for v in (reps if k == 0 else projs):
            if x in pair and pair[0] in img and pair[1] == x and img[pair[0]] == v: continue
            if x in pair and pair[1] in img and pair[0] == x and img[pair[1]] == v: continue
            img[x] = v
            qp2 = dict(qp); ok = True
            for w in level_words[k]:
                pv = val_P(w, img); q = val[w]
                if q in qp2:
                    if qp2[q] != pv: ok = False; break
                else: qp2[q] = pv
            if ok: rec(k + 1, img, qp2)
            del img[x]
            if len(sols) >= limit: return
    rec(0, {}, {})
    return sols

if __name__ == "__main__":
    n = int(sys.argv[1])
    for pair in itertools.combinations(range(6), 2):
        t = time.time(); s = search_pair(n, pair)
        print(f"n={n}: require {names[pair[0]]} != {names[pair[1]]}: {'satisfiable' if s else 'UNSAT'} ({time.time()-t:.0f}s)", flush=True)
        if s: print("    ", {names[i]: s[0][i] for i in range(6)})
