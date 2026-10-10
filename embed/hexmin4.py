import sys, time, itertools, pickle
from pmon import Pn, projections
from hexsearch import relations, names, G, Tq
from embed import orbit_reps
ws_all, val_all, eq_all = relations(3, list(range(6)))
def wname(wd): return ''.join(names[i] for i in wd)

def sat(n, classes, pair, limit=1):
    """exists six projections with x_pair distinct satisfying the equalities in `classes`?"""
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    order = [0, 3, 1, 4, 2, 5]
    def val_P(w, img):
        r = img[w[0]]
        for i in w[1:]: r = P.mul(r, img[i])
        return r
    # per level: classes restricted to available letters with >=2 words, involving new letter
    lv = []
    for k in range(6):
        allowed = set(order[:k+1]); new = order[k]
        cls = []
        for cl in classes:
            cw = [w for w in cl if set(w) <= allowed]
            if len(cw) >= 2 and any(new in w for w in cw): cls.append(cw)
        lv.append(cls)
    sols = []
    def rec(k, img):
        if sols: return
        if k == 6: sols.append(dict(img)); return
        x = order[k]
        for v in (reps if k == 0 else projs):
            if x == pair[1] and pair[0] in img and img[pair[0]] == v: continue
            if x == pair[0] and pair[1] in img and img[pair[1]] == v: continue
            img[x] = v; ok = True
            for cw in lv[k]:
                v0 = val_P(cw[0], img)
                for w in cw[1:]:
                    if val_P(w, img) != v0: ok = False; break
                if not ok: break
            if ok: rec(k + 1, img)
            del img[x]
            if sols: return
    rec(0, {})
    return sols

if __name__ == "__main__":
    n = int(sys.argv[1]); pair = (int(sys.argv[2]), int(sys.argv[3]))
    groups = {}
    for w in ws_all: groups.setdefault(val_all[w], []).append(w)
    classes = [c for c in groups.values() if len(c) > 1]
    t = time.time(); print("full:", "SAT" if sat(n, classes, pair) else "UNSAT", f"({time.time()-t:.0f}s)", flush=True)
    current = classes[:]
    for i in sorted(range(len(current)), key=lambda i: -len(current[i])):
        trial = [c for j, c in enumerate(current) if j != i and c is not None]
        t = time.time(); s = sat(n, trial, pair)
        if not s:
            current[i] = None; print(f"removed [{wname(classes[i][0])} = ...] ({time.time()-t:.0f}s)", flush=True)
        else:
            print(f"KEEP    [{wname(classes[i][0])} = ...] ({time.time()-t:.0f}s)", flush=True)
    final = [c for c in current if c]
    print(f"\nMINIMAL RELATION SET forcing {names[pair[0]]} = {names[pair[1]]} (P_{n}):")
    for cl in final: print("  ", " = ".join(wname(w) for w in sorted(cl, key=len)))
    pickle.dump(final, open(f"hexmin4_{n}_{pair[0]}{pair[1]}.pkl", "wb"))
    # also: within each kept class, minimize the words (keep only needed pairs)
