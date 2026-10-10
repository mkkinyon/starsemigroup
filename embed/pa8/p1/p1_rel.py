import pickle, numpy as np, itertools, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
R = np.concatenate([pickle.load(open(f, 'rb')) for f in sys.argv[2:]]); R = R[np.array([len(set(r[:4])) == 4 for r in R])]
a, c, b, d, x = R.T
u = th(x, a); v = th(x, c); f = th(a, b)
D = {'a': a, 'c': c, 'b': b, 'd': d, 'x': x, 'u=xa': u, 'v=xc': v, 'f=ab': f, 'dxd': th(d, x), 'xdx': th(x, d), 'cfc': th(c, f), 'dfd': th(d, f),
     'bvb': th(b, v), 'dvd': th(d, v), 'ava': th(a, v), 'bub': th(b, u), 'cuc': th(c, u), 'dud': th(d, u), 'ada': th(a, d), 'dad': th(d, a), 'bdb': th(b, d),
     'xfx': th(x, f), 'fxf': th(f, x), 'cdc': th(c, d), 'dcd': th(d, c), 'adxda?': th(a, th(d, x)), 'bdxdb': th(b, th(d, x)), 'cdxdc': th(c, th(d, x))}
K = list(D)
eqs = {(p, q) for p, q in itertools.combinations(K, 2) if np.all(D[p] == D[q])}
print("instances", len(R)); print("EQUAL:", sorted(eqs))
print("LE:", [(p, q) for p in K for q in K if p != q and (p, q) not in eqs and (q, p) not in eqs and np.all(le[D[p], D[q]])])
print("COMM:", [(p, q) for p, q in itertools.combinations(K, 2) if (p, q) not in eqs and np.all(comm[D[p], D[q]]) and not np.all(le[D[p], D[q]]) and not np.all(le[D[q], D[p]])])
print("MATCHED:", [(p, q) for p, q in itertools.combinations(K, 2) if (p, q) not in eqs and np.all(Mt[D[p], D[q]])])
