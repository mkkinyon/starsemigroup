import pickle, numpy as np, itertools
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
paths = np.array([(a, b, c, d) for a in range(N) for b in nb[a] for c in nb[b] for d in nb[c]])
closed = Mt[paths[:, 0], paths[:, 3]]
# Q instances: a=p0,c=p1,b=p2,d=p3 ; x~a, th_c(x)=th_d(x); y~a, y~b, th_y(c)=th_y(b)
rows = []
for a, c, b, d in paths:
    xs = ar[comm[ar, a] & (th(c, ar) == th(d, ar))]; ys = ar[comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))]
    if len(xs) and len(ys):
        X, Y = np.meshgrid(xs, ys, indexing='ij'); X = X.ravel(); Y = Y.ravel()
        rows.append(np.stack([np.full_like(X, a), np.full_like(X, c), np.full_like(X, b), np.full_like(X, d), X, Y], 1))
R = np.concatenate(rows); a, c, b, d, x, y = R.T
print("instances", len(R), "closed", Mt[a, d].all())
e = th(c, d)
tests = {'cd=dc': comm[c, d], 'th_a(cd)=th_b(cd)': th(a, e) == th(b, e), 'th_x(c)=th_x(d)': th(x, c) == th(x, d),
 'th_y(c)=th_y(d)': th(y, c) == th(y, d), 'x~y': comm[x, y], 'x~c': comm[x, c], 'x~d': comm[x, d], 'y~c': comm[y, c], 'y~d': comm[y, d],
 'th_y(x)=th_x(y)': th(y, x) == th(x, y), 'cd<=x': le[e, x], 'cd<=y': le[e, y], 'th_x(cd)=th_x(c)': th(x, e) == th(x, c),
 'th_a(x)=th_a(xcd)': th(a, x) == th(a, th(x, e)), 'th_c(x)<=d': le[th(c, x), d], 'th_a(y)~b? ya~b': comm[th(y, a), b],
 'th_y(a)=th_y(d)?': th(y, a) == th(y, d), 'a~d': comm[a, d], 'a~b': comm[a, b], 'th_a(c)... a<=?': le[a, c]}
for k, v in tests.items(): print(f"{k:22s} fails {np.count_nonzero(~v)}")
# which non-closed paths satisfy the hypotheses minus one atom? (to see what each hypothesis prevents) -- skip
pickle.dump(R, open('instQ4.pkl', 'wb'))
