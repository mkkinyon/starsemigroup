import pickle, numpy as np
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
rows = []
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                xs = ar[comm[ar, a] & (th(c, ar) == th(d, ar))]
                if not len(xs): continue
                ys = ar[comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))]
                if not len(ys): continue
                us = np.unique(th(a, xs)); assert (le[us, a] & (th(c, us) == th(d, us))).all()
                rows.append((a, c, b, d, tuple(us), tuple(ys)))
print("paths", len(rows), "distinct", sum(len({r[0],r[1],r[2],r[3]}) == 4 for r in rows))
pickle.dump(rows, open('instQ4.pkl', 'wb'))
