import pickle, numpy as np, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
fails = {}; cnt = 0
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    for y in ys:
        cnt += 1; v = th(b, y); f = th(a, y)
        tests = {'v c v = v': th(v, c) == v, 'v d v = v': th(v, d) == v, 'th_c(v) = th_d(v)': th(c, v) == th(d, v), 'th_c(v)=th_a(v)?': th(c, v) == th(a, v),
                 'th_c(f) = th_d(f)': th(c, f) == th(d, f), 'th_c(f)=th_b(f)': th(c, f) == th(b, f), 'th_b(f)=th_d(f)': th(b,f)==th(d,f), 'f~b': comm[f, b], 'v~a': comm[v, a],
                 'th_c(v) <= y': le[th(c, v), y], 'th_c(v) = th_y(c)?': th(c, v) == th(y, c), 'th_c(v)= th_c(y)': th(c, v) == th(c, y), 'th_a(v)=th_a(y)': th(a,v)==th(a,y),
                 'th_c(f) = th_c(y)': th(c, f) == th(c, y), 'th_d(f)=th_d(y)': th(d,f)==th(d,y), 'th_b(f)=th_b(y)': th(b,f)==th(b,y), 'th_v(f)=th_f(v)': th(v,f)==th(f,v)}
        for k, val in tests.items():
            if not val: fails[k] = fails.get(k, 0) + 1
print(n, cnt, {k: v for k, v in sorted(fails.items())})
