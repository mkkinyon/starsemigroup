import pickle, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
memo = {}
def m(*ps):
    r = P[ps[0]]
    for q in ps[1:]:
        k = (r, q)
        if k not in memo: memo[k] = mul(r, P[q], n)
        r = memo[k]
    return r
fails = {}; cnt = 0
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    for y in ys:
        cnt += 1
        tests = {'y aba y = y a y': m(y,a,b,a,y) == m(y,a,y), 'y bab y = y b y': m(y,b,a,b,y) == m(y,b,y), 'y ada y = y a y': m(y,a,d,a,y) == m(y,a,y),
                 'y dad y = y d y': m(y,d,a,d,y) == m(y,d,y), 'y aca y = yay': m(y,a,c,a,y)==m(y,a,y), 'y cac y = ycy': m(y,c,a,c,y)==m(y,c,y),
                 'y ad y = y ab y': m(y,a,d,y) == m(y,a,b,y), 'y da y = y ba y': m(y,d,a,y) == m(y,b,a,y), 'y ab y = y ac y': m(y,a,b,y)==m(y,a,c,y),
                 'y ba y = y ca y': m(y,b,a,y) == m(y,c,a,y), 'yay|><|yby': m(y,a,y,b,y,a,y)==m(y,a,y) and m(y,b,y,a,y,b,y)==m(y,b,y),
                 'y d = y b d': m(y,d) == m(y,b,d), 'd y = d b y': m(d,y) == m(d,b,y), 'y c = y b c': m(y,c) == m(y,b,c), 'y a d = y a b d': m(y,a,d)==m(y,a,b,d),
                 'y c b = y b': m(y,c,b)==m(y,b), 'y d b = y b': m(y,d,b) == m(y,b), 'y b d = y d?': m(y,b,d)==m(y,d)}
        for k, v in tests.items():
            if not v: fails[k] = fails.get(k, 0) + 1
    for u in us:
        tests = {'u d u = u?': m(u,d,u)==P[u], 'u c u = u': m(u,c,u)==P[u], 'u da u = u': m(u,d,a,u)==P[u], 'a u d = u d': m(a,u,d)==m(u,d), 'd u = d c u?': m(d,u)==m(d,c,u), 'd u = d b c u': m(d,u)==m(d,b,c,u)}
        for k, v in tests.items():
            if not v: fails[k] = fails.get(k, 0) + 1
print(n, cnt, fails)
