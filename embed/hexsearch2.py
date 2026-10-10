"""Faster search: six projections in P_n satisfying all length<=L relations of Q_0's generators."""
import sys, time, itertools, pickle
from pmon import Pn, projections
from hexsearch import relations, names, G, Tq
from embed import orbit_reps

def search(n, L=3, verbose=True):
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    order = [0, 3, 1, 4, 2, 5]
    ws, val, eq = relations(L, list(range(6)))
    # for each level k: the words whose letters are within order[:k+1] and involve order[k]
    level_words = []
    for k in range(6):
        allowed = set(order[:k + 1]); new = order[k]
        level_words.append([w for w in ws if set(w) <= allowed and new in w])
    # equality constraints: for each word, the Q-value; we maintain map Qval -> Pval
    def val_P(w, img):
        r = img[w[0]]
        for i in w[1:]: r = P.mul(r, img[i])
        return r
    sols = []; nodes = [0]
    def rec(k, img, qp):
        if sols: return
        if k == 6: sols.append(dict(img)); return
        x = order[k]
        cands = reps if k == 0 else projs
        for v in cands:
            if v in img.values(): continue
            img[x] = v; nodes[0] += 1
            qp2 = dict(qp); ok = True; seen = set(qp.values())
            for w in level_words[k]:
                pv = val_P(w, img); q = val[w]
                if q in qp2:
                    if qp2[q] != pv: ok = False; break
                else:
                    if pv in seen: ok = False; break
                    qp2[q] = pv; seen.add(pv)
            if ok: rec(k + 1, img, qp2)
            del img[x]
            if sols: return
    rec(0, {}, {})
    if verbose: print(f"    nodes: {nodes[0]}", flush=True)
    return sols

if __name__ == "__main__":
    L = int(sys.argv[2])
    for n in range(2, int(sys.argv[1]) + 1):
        t = time.time(); s = search(n, L)
        print(f"n={n}, L={L}: {'FOUND' if s else 'none'} ({time.time()-t:.0f}s)", flush=True)
        if s:
            for i, nm in enumerate(names): print("  ", nm, s[0][i])
            break
