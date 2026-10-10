import pickle, numpy as np, sys, time
sys.path.insert(0, '/home/claude/pa8w/rp')
from hq import structure, cls, show
from t12 import kappas
n = 5; P, T = pickle.load(open('/home/claude/pa8w/gen/tab5.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); Mt = (T.T == ar[:, None]) & (T == ar[None, :]); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
y0 = next(i for i in range(N) if len(P[i]) == 2 and len(list(P[i])[0]) == n)
rng = np.random.default_rng(11); stats = {}; ex = {}; cnt = 0; t0 = time.time()
while cnt < 30000:
    a = rng.integers(N)
    if not len(nb[a]): continue
    c = rng.choice(nb[a]); b = rng.choice(nb[c]); d = rng.choice(nb[b])
    if len({a,c,b,d}) < 4: continue
    us = ar[le[ar, a] & (th(c, ar) == th(d, ar))]
    if not len(us): continue
    cnt += 1
    hy = (comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))).any()
    for u in us:
        s = structure(P, n, a, c, b, d, u, y0)
        for (idx, lab, AG, CG) in s.groups:
            if not lab or len(idx) < 2: continue
            GG = cls(CG, s.Pi1)
            for kap in kappas(s, GG):
                alpha = [i for i in idx if any(E & s.match[i][0] for E in kap if E in s.Nc)]
                Ds = [k for k in idx if any(F & s.match[k][3] for F in kap if F in s.Na)]
                T1 = len(Ds) <= 1; T2 = not (alpha and Ds and alpha != Ds)
                key = ('y' if hy else 'noy', 'T1', T1, 'T2', T2); stats[key] = stats.get(key, 0) + 1
                if key not in ex: ex[key] = (a, c, b, d, u, idx)
print(cnt, f"({time.time()-t0:.0f}s)")
for k in sorted(stats): print(stats[k], k)
for k, (a, c, b, d, u, idx) in ex.items():
    if not k[4]:
        s = structure(P, n, a, c, b, d, u, y0); print('--- T2 fails', k, sorted(idx))
        for nm, i in zip('acbdu', (a, c, b, d, u)): print(f"  {nm} = {show(P, n, i)}")
        print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match]); break
