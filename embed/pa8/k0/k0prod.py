"""Test product identities in P_4 on the K0 instances (k0inst4.pkl)."""
import pickle, sys, itertools
sys.path.insert(0, '/home/claude/pa8w/review3/review-scripts')
import pm
n = 4
inst = pickle.load(open('k0inst4.pkl', 'rb'))
def P(x): return pm.proj_to_partition(x, n)
M = lambda *xs: _mul(xs)
def _mul(xs):
    r = xs[0]
    for x in xs[1:]: r = pm.mul(r, x, n)
    return r
ids = {
 'yz=yaz': lambda a,b,c,y,z: M(y,z) == M(y,a,z),
 'zy=zay': lambda a,b,c,y,z: M(z,y) == M(z,a,y),
 'yz=ybz': lambda a,b,c,y,z: M(y,z) == M(y,b,z),
 'yz=ycz': lambda a,b,c,y,z: M(y,z) == M(y,c,z),
 'zyz=zaz': lambda a,b,c,y,z: M(z,y,z) == M(z,a,z),
 'yzy=yay': lambda a,b,c,y,z: M(y,z,y) == M(y,a,y),
 'yzy=yby': lambda a,b,c,y,z: M(y,z,y) == M(y,b,y),
 'yz=yazb': lambda a,b,c,y,z: M(y,z) == M(y,a,z,b),
 'azb=azab': lambda a,b,c,y,z: M(a,z,b) == M(a,z,a,b),
 'az=azb': lambda a,b,c,y,z: M(a,z) == M(a,z,b),
 'ab=azb': lambda a,b,c,y,z: M(a,b) == M(a,z,b),
 'aya=a': lambda a,b,c,y,z: M(a,y,a) == a,
 'ay=ya': lambda a,b,c,y,z: M(a,y) == M(y,a),
 'yab=yb': lambda a,b,c,y,z: M(y,a,b) == M(y,b),
 'yab=yba': lambda a,b,c,y,z: M(y,a,b) == M(y,b,a),
 'yaz=yza': lambda a,b,c,y,z: M(y,a,z) == M(y,z,a),
 'zay=zya': lambda a,b,c,y,z: M(z,a,y) == M(z,y,a),
 'yzb=yab': lambda a,b,c,y,z: M(y,z,b) == M(y,a,b),
 'azy=ay': lambda a,b,c,y,z: M(a,z,y) == M(a,y),
 'yza=ya': lambda a,b,c,y,z: M(y,z,a) == M(y,a),
 'cz=czc': lambda a,b,c,y,z: M(c,z) == M(c,z,c),
 'cy=yc': lambda a,b,c,y,z: M(c,y) == M(y,c),
 'czb=cb': lambda a,b,c,y,z: M(c,z,b) == M(c,b),
 'azc=ac': lambda a,b,c,y,z: M(a,z,c) == M(a,c),
 'yzc=yc': lambda a,b,c,y,z: M(y,z,c) == M(y,c),
 'yzc=yac': lambda a,b,c,y,z: M(y,z,c) == M(y,a,c),
}
fails = {k: 0 for k in ids}
ex = {}
for d in inst:
    a,b,c,y,z = (P(d[k]) for k in 'abcyz')
    for k, f in ids.items():
        if not f(a,b,c,y,z):
            fails[k] += 1
            ex.setdefault(k, d)
for k in ids:
    print(f'{k:12s} fails {fails[k]}/{len(inst)}')
