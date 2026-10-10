import pickle, numpy as np, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
rows = pickle.load(open(sys.argv[2], 'rb'))
fails = {}; cnt = 0
for a, c, b, d, us, ys in rows:
    if len({a,c,b,d}) < 4: continue
    e = th(a, d)   # theta_a(d)
    for u in us:
        for y in ys:
            cnt += 1
            ya = th(a, y)
            tests = {'u <= e': le[u, e], 'ya <= e': le[ya, e], 'u ~ e': comm[u, e], 'ya ~ e': comm[ya, e], 'th_u(e) = u': th(u, e) == u,
                     'th_e(y) = th_a(y)': th(e, y) == ya, 'th_ya(e) = ya': th(ya, e) == ya, 'y ~ e': comm[y, e], 'th_e(u)=u': th(e,u)==u,
                     'e = a': e == a, 'th_d(a) ~ d?': True}
            for k, v in tests.items():
                if not v: fails[k] = fails.get(k, 0) + 1
print(n, cnt, fails)
