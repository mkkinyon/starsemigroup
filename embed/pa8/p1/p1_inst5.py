import pickle, numpy as np, time, sys
P, T = pickle.load(open('/home/claude/pa8w/gen/tab5.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]
Mt = (T.T == ar[:, None]) & (T == ar[None, :]); comm = (T == T.T)
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
rng = np.random.default_rng(int(sys.argv[1])); rows = []; t0 = time.time(); npaths = 0
while npaths < int(sys.argv[2]):
    a = rng.integers(N)
    if not len(nb[a]): continue
    c = rng.choice(nb[a]); b = rng.choice(nb[c]); d = rng.choice(nb[b])
    if len({a, c, b, d}) < 4: continue
    npaths += 1
    xs = ar[comm[ar, a] & comm[ar, c] & (th(a, ar) == th(b, ar)) & (th(ar, c) == th(ar, d))]
    for x in xs: rows.append((a, c, b, d, x))
R = np.array(rows); print("paths", npaths, "instances", len(R), "closed", Mt[R[:, 0], R[:, 3]].all(), f"({time.time()-t0:.0f}s)")
pickle.dump(R, open(f'instP5_{sys.argv[1]}.pkl', 'wb'))
