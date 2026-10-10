import pickle, numpy as np, itertools, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
R = pickle.load(open(f'instE{n}.pkl', 'rb')); a, b, c, d = R.T
sel = (a != b) & (c != d) & (a != c) & (a != d) & (b != c) & (b != d); a, b, c, d = a[sel], b[sel], c[sel], d[sel]
e = th(c, d)
D = {'a': a, 'b': b, 'c': c, 'd': d, 'e=cd': e, 'aea': th(a, e), 'bcb': th(b, c), 'bdb': th(b, d), 'beb': th(b, e), 'cac': th(c, a), 'dad': th(d, a),
     'eae': th(e, a), 'cbc': th(c, b), 'dbd': th(d, b), 'ebe': th(e, b), 'aba': th(a, b), 'bab': th(b, a), 'aca': th(a, c), 'ada': th(a, d), 'cec': th(c, e)}
K = list(D)
eqs = {(p, q) for p, q in itertools.combinations(K, 2) if np.all(D[p] == D[q])}
print("instances", len(a)); print("EQUAL:", sorted(eqs))
print("LE:", [(p, q) for p in K for q in K if p != q and (p, q) not in eqs and (q, p) not in eqs and np.all(le[D[p], D[q]])])
print("COMM:", [(p, q) for p, q in itertools.combinations(K, 2) if (p, q) not in eqs and np.all(comm[D[p], D[q]]) and not np.all(le[D[p], D[q]]) and not np.all(le[D[q], D[p]])])
print("MATCHED:", [(p, q) for p, q in itertools.combinations(K, 2) if (p, q) not in eqs and np.all(Mt[D[p], D[q]])])
