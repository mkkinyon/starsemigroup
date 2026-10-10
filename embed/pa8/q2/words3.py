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
    cnt += 1
    tests = {'cad = cbd': m(c,a,d) == m(c,b,d), 'cad = cd': m(c,a,d) == m(c,d), 'cad = cacd?': m(c,a,d)==m(c,a,c,d), 'dac = dbc': m(d,a,c)==m(d,b,c),
             'bad = bcad': m(b,a,d) == m(b,c,a,d), 'bad = bd': m(b,a,d)==m(b,d), 'cbad = cbd': m(c,b,a,d)==m(c,b,d), 'ad = acbd': m(a,d)==m(a,c,b,d),
             'cadb = cb?': m(c,a,d,b)==m(c,b), 'c ad c = c d c': m(c,a,d,c)==m(c,d,c), 'd a d = d c d?': m(d,a,d)==m(d,c,d), 'dad = dcbd?': m(d,a,d)==m(d,c,b,d),
             'ada = acbda?': m(a,d,a)==m(a,c,b,d,a), 'a d b = a c b': m(a,d,b)==m(a,c,b), 'adc = ac': m(a,d,c)==m(a,c), 'b d a = b c a': m(b,d,a)==m(b,c,a),
             'cda = ca': m(c,d,a)==m(c,a), 'c d a = c b d a?': m(c,d,a)==m(c,b,d,a), 'dca = da': m(d,c,a)==m(d,a), 'dcba = da': m(d,c,b,a)==m(d,a)}
    for k, v in tests.items():
        if not v: fails[k] = fails.get(k, 0) + 1
print(n, cnt, {k: v for k, v in sorted(fails.items())})
