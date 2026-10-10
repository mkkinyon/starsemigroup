import itertools, pickle, random
from pmon import partition_monoid, Pn, star
n = 3
P = Pn(n); elems = partition_monoid(n)
letters = ['x', 'X', 'y', 'Y']   # X = x*, Y = y*
words = [w for L in range(1, 5) for w in itertools.product(letters, repeat=L)]
def ev(w, x, y, mul, st):
    val = {'x': x, 'X': st(x), 'y': y, 'Y': st(y)}
    r = val[w[0]]
    for c in w[1:]:
        r = mul(r, val[c])
    return r
# partition words by equality over many random pairs in P_3
random.seed(1)
classes = {w: 0 for w in words}
# refine: key = tuple of values on samples
samples = [(random.choice(elems), random.choice(elems)) for _ in range(400)]
keys = {}
for w in words:
    keys[w] = tuple(ev(w, x, y, P.mul, P.star) for x, y in samples)
groups = {}
for w in words:
    groups.setdefault(keys[w], []).append(w)
ids = [g for g in groups.values() if len(g) > 1]
print("identity classes (P_3, sampled):", len(ids), "nontrivial;", sum(len(g) for g in ids), "words involved")
# check on all regular *-semigroups of order <= 7 whether these identities hold
allres = pickle.load(open("rss_nontriv7.pkl", "rb"))
bad = 0
for order in sorted(allres):
    for T, st in allres[order]:
        m = len(T)
        mul = lambda a, b: T[a][b]; s = lambda a: st[a]
        for g in ids:
            for x in range(m):
                for y in range(m):
                    vals = {ev(w, x, y, mul, s) for w in g}
                    if len(vals) > 1:
                        bad += 1; break
                else: continue
                break
            else: continue
            break
print("semigroups of order<=7 violating some sampled P_3-identity:", bad)
