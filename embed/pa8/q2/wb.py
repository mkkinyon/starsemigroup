import pickle, numpy as np, sys
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
stats = {}
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    ws = ar[le[ar, b] & (th(c, ar) == th(d, ar))]
    ws2 = ar[le[ar, d] & (th(b, ar) == th(a, ar))]   # reversed-path u: w <= d, th_b(w) = th_a(w)
    ws3 = ar[comm[ar, d] & comm[ar, c] & (th(ar, b) == th(ar, c))]  # reversed-path y
    k = ('w<=b th_c=th_d', bool(len(ws)), 'w<=d th_b=th_a', bool(len(ws2)), 'y rev', bool(len(ws3))); stats[k] = stats.get(k, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
