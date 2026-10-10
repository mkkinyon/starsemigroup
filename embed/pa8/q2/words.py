import pickle, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
n = int(sys.argv[1]); files = sys.argv[2:]
P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
memo = {}
def m(*ps):
    r = P[ps[0]]
    for q in ps[1:]:
        k = (r, q)
        if k not in memo: memo[k] = mul(r, P[q], n)
        r = memo[k]
    return r
fails = {}; cnt = 0
for a, c, b, d, us, ys in pickle.load(open(files[0], 'rb')):
    if len({a,c,b,d}) < 4: continue
    for u in us:
        cnt += 1
        tests = {'ud = ucbd': m(u, d) == m(u, c, b, d), 'ud = ucd': m(u, d) == m(u, c, d), 'uc = ud?': m(u, c) == m(u, d),
                 'ucb = ud?': m(u, c, b) == m(u, d), 'ucbd = ucd': m(u, c, b, d) == m(u, c, d)}
        for k, v in tests.items():
            if not v: fails[k] = fails.get(k, 0) + 1
    for y in ys:
        tests = {'y ad = y acbd': m(y, a, d) == m(y, a, c, b, d), 'ad y = acbd y': m(a, d, y) == m(a, c, b, d, y), 'y ad = y abd': m(y, a, d) == m(y, a, b, d),
                 'ad y = ad y?': True, 'ya d = ya bd': m(y, a, d) == m(y, a, b, d), 'yb d = yb': m(y,b,d) == m(y,b), 'yc = yb?': m(y, c) == m(y, b), 'ycb = yb': m(y, c, b) == m(y, b), 'y c d = y b': m(y,c,d)==m(y,b)}
        for k, v in tests.items():
            if not v: fails[k] = fails.get(k, 0) + 1
print(n, "instances(u)", cnt, fails)
