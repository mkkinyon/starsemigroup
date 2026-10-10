import sys, time, pickle
from pmon import Pn, projections
from hexsearch import relations, names, G, Tq
from embed import orbit_reps
ws_all, val_all, eq_all = relations(3, list(range(6)))
def wname(wd): return ''.join(names[i] for i in wd)

def search_eq(n, classes, extra_distinct=None):
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    order = [0, 3, 1, 4, 2, 5]
    def val_P(w, img):
        r = img[w[0]]
        for i in w[1:]: r = P.mul(r, img[i])
        return r
    def check(img):
        letters = set(img)
        for cl in classes:
            cw = [w for w in cl if set(w) <= letters]
            if len(cw) < 2: continue
            v = val_P(cw[0], img)
            for w in cw[1:]:
                if val_P(w, img) != v: return False
        return True
    sols = []
    def rec(k, img):
        if sols: return
        if k == 6: sols.append(dict(img)); return
        x = order[k]
        for v in (reps if k == 0 else projs):
            if v in img.values(): continue      # six letters pairwise distinct
            img[x] = v
            if check(img): rec(k + 1, img)
            del img[x]
            if sols: return
    rec(0, {})
    return sols

if __name__ == "__main__":
    n = int(sys.argv[1])
    groups = {}
    for w in ws_all: groups.setdefault(val_all[w], []).append(w)
    classes = [c for c in groups.values() if len(c) > 1]
    t = time.time(); s = search_eq(n, classes); print("full:", "FOUND" if s else "none", f"({time.time()-t:.0f}s)", flush=True)
    current = classes[:]
    for i in sorted(range(len(current)), key=lambda i: -len(current[i])):
        trial = [c for j, c in enumerate(current) if j != i and c is not None]
        t = time.time(); s = search_eq(n, trial)
        if not s:
            current[i] = None; print(f"removed [{wname(current_cl[0]) if (current_cl:=classes[i]) else ''}...] ({time.time()-t:.0f}s)", flush=True)
        else:
            print(f"keep    [{wname(classes[i][0])} = ...] ({time.time()-t:.0f}s)", flush=True)
    final = [c for c in current if c]
    print("\nMINIMAL RELATION SET (P_%d):" % n)
    for cl in final: print("  ", " = ".join(wname(w) for w in sorted(cl, key=len)))
    pickle.dump(final, open(f"hexmin_{n}.pkl", "wb"))
