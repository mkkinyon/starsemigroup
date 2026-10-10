import pickle, numpy as np, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
def validu(a, c, d, w): return le[w, a] and th(c, w) == th(d, w)
def validy(a, c, b, w): return comm[w, a] and comm[w, b] and th(w, c) == th(w, b)
fails = {}; cnt = 0
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    for u in us:
        for y in ys:
            cnt += 1; f = th(a, y); v = th(b, y)
            tests = {'u~y': comm[u, y], 'u~f=ya': comm[u, f], 'th_f(u) valid u': validu(a, c, d, th(f, u)), 'th_u(f) valid u': validu(a, c, d, th(u, f)),
                     'f valid u': validu(a, c, d, f), 'u valid y': validy(a, c, b, u), 'th_y(u) valid y': validy(a, c, b, th(y, u)), 'th_u(y) valid y': validy(a, c, b, th(u, y)),
                     'th_y(u) valid u': validu(a, c, d, th(y, u)), 'u~v': comm[u, v], 'th_c(u)~v': comm[th(c,u), v], 'z=th_c(u) <= v?': le[th(c, u), v], 'th_v(z) = z?': th(v, th(c,u)) == th(c,u),
                     'th_z(v)=v?': th(th(c,u), v) == v, 'th_y(z)=th_y(u)?': th(y, th(c, u)) == th(y, u), 'th_y(u)=th_y(uc..)': True, 'th_b(z) valid?': True,
                     'th_a(v)=?u': th(a, v) == u, 'th_a(v) valid u': validu(a, c, d, th(a, v)), 'th_a(v)~u': comm[th(a, v), u], 'th_a(v) <= f': le[th(a, v), f]}
            for k, val in tests.items():
                if not val: fails[k] = fails.get(k, 0) + 1
print(n, cnt, {k: v for k, v in sorted(fails.items())})
