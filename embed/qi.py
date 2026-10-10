"""Test quasi-identities on P_n: hypotheses = list of (word, word) equalities over projection
variables; conclusion = (word, word) equality. Report whether hyps & (u != v) is satisfiable."""
import sys, time, itertools
from pmon import Pn, projections
from embed import orbit_reps

def test_qi(n, letters, hyps, concl, limit=1, verbose=False):
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
    sols = []
    def rec(k, img):
        if sols: return
        if k == len(order):
            if val(concl[0], img) != val(concl[1], img): sols.append(dict(img))
            return
        x = order[k]
        for v in (reps if k == 0 else projs):
            img[x] = v
            if all(val(u, img) == val(w, img) for (u, w) in lv[k]):
                rec(k + 1, img)
            del img[x]
            if sols: return
    rec(0, {})
    return sols

if __name__ == "__main__":
    n = int(sys.argv[1])
    tests = {
      # (letters, hyps, conclusion)
      "H1,H4,H6 => z=m": ("abcd",   # a=a0, b=b0, c=b1, d=b2
          [("aca","a"),("ada","a"),("cac","c"),
           ("bca","bda"),("bca","cab"),("bca","cba"),("bca","cda"),("bca","dab"),("bca","dba"),("bca","dca")],
          ("bc","ab")),
      "H1,H4,H6 => a0=b0": ("abcd",
          [("aca","a"),("ada","a"),("cac","c"),
           ("bca","bda"),("bca","cab"),("bca","cba"),("bca","cda"),("bca","dab"),("bca","dba"),("bca","dca")],
          ("a","b")),
      "H1,H4,H6 => b0b1=b1b0": ("abcd",
          [("aca","a"),("ada","a"),("cac","c"),
           ("bca","bda"),("bca","cab"),("bca","cba"),("bca","cda"),("bca","dab"),("bca","dba"),("bca","dca")],
          ("bc","cb")),
    }
    for name, (letters, hyps, concl) in tests.items():
        t = time.time(); s = test_qi(n, letters, hyps, concl)
        print(f"{name}: {'NOT forced (counterexample found)' if s else 'FORCED'} in P_{n} ({time.time()-t:.0f}s)", flush=True)
        if s: print("   ", s[0])
