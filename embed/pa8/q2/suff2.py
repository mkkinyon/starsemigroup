import pickle, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, join_classes
n = 4; P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb'))
th = lambda x, p: T[p, x]
found = pickle.load(open('suff_found.pkl', 'rb'))['ycb=yb']
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def word(*idx):
    r = P[idx[0]]
    for i in idx[1:]: r = m(r, P[i])
    return r
tests = {'th_y(d)=th_y(b)': lambda a,c,b,d,y: th(y, d) == th(y, b), 'y.cd = y.b?': lambda a,c,b,d,y: word(y,c,d) == word(y,b),
         'y.c.d = y.b.d': lambda a,c,b,d,y: word(y,c,d) == word(y,b,d), 'ybc = yb?': lambda a,c,b,d,y: word(y,b,c) == word(y,b),
         'ydb = yb': lambda a,c,b,d,y: word(y,d,b) == word(y,b), 'ybd = yd?': lambda a,c,b,d,y: word(y,b,d) == word(y,d),
         'ycb=ycd?': lambda a,c,b,d,y: word(y,c,b) == word(y,c,d), 'yc = yd?': lambda a,c,b,d,y: word(y,c) == word(y,d),
         'yc = ycb?': lambda a,c,b,d,y: word(y,c) == word(y,c,b), 'th_y(c)=th_y(d)': lambda a,c,b,d,y: th(y,c)==th(y,d),
         'yac = yab?': lambda a,c,b,d,y: word(y,a,c) == word(y,a,b), 'ya c b = ya b': lambda a,c,b,d,y: word(y,a,c,b) == word(y,a,b),
         'y c y = y b y (=th)': lambda a,c,b,d,y: th(y,c)==th(y,b), 'ycy b = yby? ': lambda a,c,b,d,y: word(y,c,y,b) == word(y,b), 'ycyc = yby?': lambda a,c,b,d,y: word(y,c,y,c)==word(y,b)}
fails = {k: 0 for k in tests}
for a, c, b, d, us, y in found:
    for k, f in tests.items():
        if not f(a, c, b, d, y): fails[k] += 1
print(len(found), fails)
for a, c, b, d, us, y in found[:3]:
    print('---')
    for nm, i in zip('acbdy', (a, c, b, d, y)): print(f"  {nm} = {show(i)}")
    print("  u in:", '; '.join(show(i) for i in us), " rho:", [sorted(K) for K in join_classes([P[a], P[d]], n)])
