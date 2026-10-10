import pickle, numpy as np, itertools
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]          # theta_x(p)
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T)
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
paths = [(a, c, b, d) for a in range(N) for c in nb[a] for b in nb[c] for d in nb[b]]
print("paths", len(paths))
# sub-goals: g1: theta_a(d)=a ; g2: theta_d(a)=d
res = {}
for a, c, b, d in paths:
    g1 = th(a, d) == a; g2 = th(d, a) == d
    if g1 and g2: continue
    hx = [comm[ar, a], th(c, ar) == th(d, ar)]
    hy = [comm[ar, a], comm[ar, b], th(ar, c) == th(ar, b)]
    for drop in range(6):   # 5 = drop nothing
        ex = [h for i, h in enumerate(hx) if i != drop]; ey = [h for i, h in enumerate(hy) if i + 2 != drop]
        okx = np.logical_and.reduce(ex) if ex else np.ones(N, bool); oky = np.logical_and.reduce(ey) if ey else np.ones(N, bool)
        if okx.any() and oky.any():
            k = (drop, bool(g1), bool(g2)); res[k] = res.get(k, 0) + 1
names = ['drop xa=ax', 'drop th_c(x)=th_d(x)', 'drop ya=ay', 'drop yb=by', 'drop th_y(c)=th_y(b)', 'drop nothing']
for k in sorted(res): print(names[k[0]], "  g1", k[1], "g2", k[2], " paths:", res[k])
