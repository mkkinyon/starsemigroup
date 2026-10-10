"""Like qi.test_qi but with all letters required to be distinct."""
import time
from pmon import Pn, projections
from embed import orbit_reps

def test_qi(n, letters, hyps, concl, distinct=True, limit=None):
    P = Pn(n); projs = projections(n)
    D = type('D', (), {'n': n, 'projs': projs})(); reps = orbit_reps(D)
    order = list(letters)
    def val(w, img):
        r = img[w[0]]
        for ch in w[1:]: r = P.mul(r, img[ch])
        return r
    lv = []
    for k in range(len(order)):
        allowed = set(order[:k+1]); new = order[k]
        lv.append([(u, v) for (u, v) in hyps if set(u) | set(v) <= allowed and (new in u or new in v)])
    sols = []; t0 = time.time()
    def rec(k, img):
        if sols: return
        if limit and time.time() - t0 > limit: raise TimeoutError
        if k == len(order):
            if val(concl[0], img) != val(concl[1], img): sols.append(dict(img))
            return
        x = order[k]
        for v in (reps if k == 0 else projs):
            if distinct and v in img.values(): continue
            img[x] = v
            if all(val(u, img) == val(w, img) for (u, w) in lv[k]):
                rec(k + 1, img)
            del img[x]
            if sols: return
    try: rec(0, {})
    except TimeoutError: return "timeout"
    return sols
