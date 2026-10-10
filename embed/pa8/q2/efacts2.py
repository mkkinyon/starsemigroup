import pickle, numpy as np
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None]); Mt = (T.T == ar[:, None]) & (T == ar[None, :])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
fx = {}; fy = {}; cx = cy = 0
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                if len({a,c,b,d}) < 4: continue
                e = th(a, d); f = th(d, a)
                us = ar[le[ar, a] & (th(c, ar) == th(d, ar))]
                for u in us:
                    cx += 1
                    for k, v in {'u <= e': le[u, e], 'u ~ e': comm[u, e], 'th_c(u) <= f=th_d(a)': le[th(c, u), f], 'th_e(u) = u': th(e, u) == u, 'th_u(e)=u': th(u,e)==u,
                                 'u <= th_a(cbd)?': le[u, th(a, th(th(d, b), c))] }.items():
                        if not v: fx[k] = fx.get(k, 0) + 1
                ys = ar[comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))]
                for y in ys:
                    cy += 1; ya = th(a, y)
                    for k, v in {'ya <= e': le[ya, e], 'ya ~ e': comm[ya, e], 'y ~ e': comm[y, e], 'th_e(y)=ya': th(e, y) == ya, 'th_y(e)=th_y(a)': th(y, e) == th(y, a),
                                 'th_y(d)=th_y(b)': th(y, d) == th(y, b), 'y ~ f': comm[y, f], 'th_y(f)=th_y(d)': th(y, f) == th(y, d)}.items():
                        if not v: fy[k] = fy.get(k, 0) + 1
print("u-only instances", cx, fx); print("y-only instances", cy, fy)
