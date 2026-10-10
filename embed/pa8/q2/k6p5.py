import pickle, numpy as np, sys, time
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
n = 5; P, T = pickle.load(open('/home/claude/pa8w/gen/tab5.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); Mt = (T.T == ar[:, None]) & (T == ar[None, :]); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]; NB = [[t for t, tr in top_blocks(P[i], n) if not tr] for i in range(N)]
SUPP = [frozenset().union(*TB[i]) if TB[i] else frozenset() for i in range(N)]
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
rng = np.random.default_rng(5); t0 = time.time(); cnt = 0; res = {}; ex = {}
while cnt < 20000:
    a = rng.integers(N)
    if not len(nb[a]): continue
    c = rng.choice(nb[a]); b = rng.choice(nb[c]); d = rng.choice(nb[b])
    if len({a,c,b,d}) < 4: continue
    xs = ar[comm[ar, a] & (th(c, ar) == th(d, ar)) & le[ar, a]]
    if not len(xs): continue
    cnt += 1
    K3 = all(sum(1 for D in TB[d] if Z & D) <= 1 for Z in TB[a] + NB[a])
    UB = all(sum(1 for D in TB[d] if Z & D & SUPP[b]) <= 1 for Z in TB[a] + NB[a])
    K6 = all(sum(1 for A in TB[a] if A & D) <= 1 for D in TB[d])
    K6b = all(sum(1 for A in TB[a] if A & D & SUPP[b]) <= 1 for D in TB[d])
    K6c = all(sum(1 for A in TB[a] if A & D & SUPP[c]) <= 1 for D in TB[d])
    k = (K3, UB, K6, K6b, K6c); res[k] = res.get(k, 0) + 1
    if k not in ex: ex[k] = (a, c, b, d, xs)
print("x-only paths", cnt, f"({time.time()-t0:.0f}s)")
for k in sorted(res): print(" K3", k[0], "U-B", k[1], "K6", k[2], "K6b", k[3], "K6c", k[4], ":", res[k])
for k, (a, c, b, d, xs) in ex.items():
    if not k[2]:
        print('--- K6 fails'); 
        for nm, i in zip('acbd', (a, c, b, d)): print(f"  {nm} = {show(i)}")
        print("  u in:", '; '.join(show(i) for i in xs)); break
