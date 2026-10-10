import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]; comm = (T == T.T); Mt = (T.T == ar[:, None]) & (T == ar[None, :])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]; NB = [[t for t, tr in top_blocks(P[i], n) if not tr] for i in range(N)]
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
def K3(a, d): return all(sum(1 for D in TB[d] if Z & D) <= 1 for Z in TB[a] + NB[a])
def K6(a, d): return all(sum(1 for A in TB[a] if A & D) <= 1 for D in TB[d])
res = {}; ex = {}
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                if len({a,c,b,d}) < 4: continue
                hx = (comm[ar, a] & (th(c, ar) == th(d, ar))).any(); hy = (comm[ar, a] & comm[ar, b] & (th(ar, c) == th(ar, b))).any()
                k = (hx, hy, K3(a, d), K6(a, d)); res[k] = res.get(k, 0) + 1
                if k not in ex: ex[k] = (a, c, b, d)
for k in sorted(res): print("x-witness", k[0], "y-witness", k[1], " K3", k[2], "K6", k[3], ":", res[k])
for k in [(True, False, False, True), (True, False, True, False), (False, True, False, True), (False, True, True, False), (True, False, False, False)]:
    if k in ex:
        print('---', k); 
        for nm, i in zip('acbd', ex[k]): print(f"  {nm} = {show(i)}")
