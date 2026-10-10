import pickle, numpy as np, itertools
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
R = pickle.load(open('instQ4.pkl', 'rb')); a, c, b, d, x, y = R.T
D = {'a': a, 'c': c, 'b': b, 'd': d, 'x': x, 'y': y, 'u=ya': th(y, a), 'w=yb': th(y, b), 'e=cd': th(c, d), 't=cxc': th(c, x), 'v=xa': th(x, a),
     's=xcx': th(x, c), 'ax a': th(a, x), 'bxb': th(b, x), 'yxy': th(y, x), 'xyx': th(x, y), 'aba': th(a, b), 'bab': th(b, a), 'ada': th(a, d), 'dad': th(d, a),
     'ceac=ae? aea': th(a, th(c, d)), 'beb': th(b, th(c, d)), 'ded': th(d, th(c, d))}
K = list(D)
print("EQUAL:", [(p, q) for p, q in itertools.combinations(K, 2) if np.all(D[p] == D[q])])
eqs = {(p, q) for p, q in itertools.combinations(K, 2) if np.all(D[p] == D[q])}
print("LE (p<=q):", [(p, q) for p in K for q in K if p != q and (p, q) not in eqs and (q, p) not in eqs and np.all(le[D[p], D[q]])])
print("COMM:", [(p, q) for p, q in itertools.combinations(K, 2) if (p, q) not in eqs and np.all(comm[D[p], D[q]]) and not np.all(le[D[p], D[q]]) and not np.all(le[D[q], D[p]])])
print("MATCHED:", [(p, q) for p, q in itertools.combinations(K, 2) if (p, q) not in eqs and np.all(Mt[D[p], D[q]])])
