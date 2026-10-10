import pickle, numpy as np, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
def validyrev(a, c, b, d, w): return bool(comm[w, d] and comm[w, c] and th(w, b) == th(w, c))
fails = {}; cnt = 0
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    for u in us:
        z = th(c, u)
        for y in ys:
            cnt += 1; v = th(y, b)
            cands = {'z': z, 'th_c(y)': th(c, y), 'th_d(y)': th(d, y), 'v=th_y(b)': v, 'th_z(y)': th(z, y), 'th_y(z)': th(y, z), 'th_c(v)': th(c, v), 'th_z(v)': th(z, v), 'th_v(z)': th(v, z),
                     'th_d(v)': th(d, v), 'th_c(th_d(y))': th(c, th(d, y)), 'z*v?': th(v, z)}
            for k, w in cands.items():
                if not validyrev(a, c, b, d, w): fails[k] = fails.get(k, 0) + 1
print(n, cnt, {k: v for k, v in sorted(fails.items())})
