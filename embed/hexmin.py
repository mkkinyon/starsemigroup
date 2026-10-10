import sys, time, itertools
from pmon import Pn, projections
from hexsearch import relations, names, G, Tq, word_val_Q
from embed import orbit_reps
ws_all, val_all, eq_all = relations(3, list(range(6)))
def wname(wd): return ''.join(names[i] for i in wd)

def search_with(n, classes, distinct=True):
    """classes: list of lists of words that must be equal; words in different classes (among the
    listed words) must be distinct if distinct=True."""
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    order = [0, 3, 1, 4, 2, 5]
    def val_P(w, img):
        r = img[w[0]]
        for i in w[1:]: r = P.mul(r, img[i])
        return r
    def check(img):
        letters = set(img)
        reps_ = []
        for cl in classes:
            cw = [w for w in cl if set(w) <= letters]
            if not cw: continue
            v = val_P(cw[0], img)
            for w in cw[1:]:
                if val_P(w, img) != v: return False
            reps_.append(v)
        if distinct and len(set(reps_)) != len(reps_): return False
        return True
    sols = []
    def rec(k, img):
        if sols: return
        if k == 6: sols.append(dict(img)); return
        x = order[k]
        for v in (reps if k == 0 else projs):
            if v in img.values(): continue
            img[x] = v
            if check(img): rec(k + 1, img)
            del img[x]
            if sols: return
    rec(0, {})
    return sols

if __name__ == "__main__":
    n = int(sys.argv[1])
    # all classes including singletons (for distinctness)
    groups = {}
    for w in ws_all: groups.setdefault(val_all[w], []).append(w)
    classes = list(groups.values())
    t = time.time(); print("full:", "FOUND" if search_with(n, classes) else "none", f"({time.time()-t:.0f}s)", flush=True)
    # try removing each nontrivial class (merge its words into singletons) 
    for idx, cl in enumerate(classes):
        if len(cl) < 2: continue
        cl2 = [c for j, c in enumerate(classes) if j != idx] + [[w] for w in cl]
        t = time.time(); s = search_with(n, cl2)
        print(f"without class [{wname(cl[0])}...]: {'FOUND' if s else 'none'} ({time.time()-t:.0f}s)", flush=True)
