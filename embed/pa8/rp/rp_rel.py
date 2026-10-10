"""Order/commutation relations among derived projections in all (R') instances of P_4."""
import sys, pickle, itertools
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import mul
n = 4; inst = pickle.load(open('inst4.pkl', 'rb'))
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
names = ['a','b','c','x','y','u=ya','v=xc','r=xbx','m=xy','t=axa','s=cyc?','w=byb?']
def derived(I):
    a, c, b, x, y = I
    u = m(y, a); v = m(x, c); r = th(x, b); mm = m(x, y); t = th(a, x)
    return {'a':a,'b':b,'c':c,'x':x,'y':y,'u':u,'v':v,'r':r,'m':mm,'t':t,'bvb':th(b,v),'axb':None}
keys = ['a','b','c','x','y','u','v','r','m','t','bvb']
rel = {}
for (p, q) in itertools.permutations(keys, 2):
    rel[('le', p, q)] = True; rel[('comm', p, q)] = True; rel[('match', p, q)] = True; rel[('eq', p, q)] = True
    rel[('thpq_eq_q', p, q)] = True  # theta_p(q) = ... skip
for I in inst:
    d = derived(I)
    for (p, q) in itertools.permutations(keys, 2):
        P, Q = d[p], d[q]
        if rel[('le', p, q)] and th(Q, P) != P: rel[('le', p, q)] = False
        if rel[('comm', p, q)] and m(P, Q) != m(Q, P): rel[('comm', p, q)] = False
        if rel[('match', p, q)] and not (th(P, Q) == P and th(Q, P) == Q): rel[('match', p, q)] = False
        if rel[('eq', p, q)] and P != Q: rel[('eq', p, q)] = False
print("equal:", sorted((p, q) for (k, p, q), v in rel.items() if k == 'eq' and v and p < q))
print("p <= q:", sorted((p, q) for (k, p, q), v in rel.items() if k == 'le' and v and not rel[('eq', p, q)]))
print("commute:", sorted((p, q) for (k, p, q), v in rel.items() if k == 'comm' and v and p < q and not rel[('le', p, q)] and not rel[('le', q, p)]))
print("matched:", sorted((p, q) for (k, p, q), v in rel.items() if k == 'match' and v and p < q))
