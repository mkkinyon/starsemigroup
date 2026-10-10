"""Search P_n for six pairwise-distinct projections satisfying all length<=L *equalities* of Q_0
(no other distinctness required). Report coincidences among the named elements."""
import sys, time, itertools
from pmon import Pn, projections
from hexsearch import relations, names, G, Tq
from embed import orbit_reps

def search(n, L=3, need_distinct=True, limit=5):
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
        if k == 6: sols.append((dict(img), dict(qp))); return
        x = order[k]
        for v in (reps if k == 0 else projs):
            if need_distinct and v in img.values(): continue
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
    return sols, val

if __name__ == "__main__":
    L = 3
    for n in range(2, int(sys.argv[1]) + 1):
        t = time.time(); sols, val = search(n, L)
        print(f"n={n}: {len(sols)} solutions with equalities only ({time.time()-t:.0f}s)", flush=True)
        for img, qp in sols[:3]:
            # which Q-elements coincide?
            inv = {}
            for q, p in qp.items(): inv.setdefault(p, []).append(q)
            merged = [v for v in inv.values() if len(v) > 1]
            z = Tq[G[3]][G[4]]; w = Tq[G[0]][G[1]]; m = [Tq[G[i]][G[3+i]] for i in range(3)]
            label = {G[i]: names[i] for i in range(6)}; label[z]='z'; label[w]='w'
            for i in range(3): label[m[i]] = f'm{i}'
            print("   coincidences:", [[label.get(q, '?') for q in v] for v in merged])
            print("   images:", {names[i]: img[i] for i in range(6)})
