import pickle, numpy as np, time, sys
P, T = pickle.load(open('/home/claude/pa8w/gen/tab6.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
rng = np.random.default_rng(int(sys.argv[1])); rows = []; t0 = time.time(); npaths = 0; tried = 0
while npaths < int(sys.argv[2]):
    a = rng.integers(N)
    if not len(nb[a]): continue
    c = rng.choice(nb[a]); b = rng.choice(nb[c]); d = rng.choice(nb[b])
    if len({a, c, b, d}) < 4: continue
    tried += 1
    xs = ar[comm[ar, a] & (th(c, ar) == th(d, ar))]
    if not len(xs): continue
    ys = ar[comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))]
    if not len(ys): continue
    us = np.unique(th(a, xs))   # theta_a(x)
    assert (comm[us, a] & (th(c, us) == th(d, us)) & le[us, a]).all()
    npaths += 1
    rows.append((a, c, b, d, tuple(us), tuple(ys)))
print("tried", tried, "paths", npaths, "closed", all(Mt[r[0], r[3]] for r in rows), f"({time.time()-t0:.0f}s)")
pickle.dump(rows, open(f'instQ6_{sys.argv[1]}.pkl', 'wb'))
