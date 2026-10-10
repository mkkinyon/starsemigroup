import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]; comm = (T == T.T); Mt = (T.T == ar[:, None]) & (T == ar[None, :]); le = (T == ar[:, None])
nb = [np.nonzero(Mt[i] & (ar != i))[0] for i in range(N)]
TB = [[t for t, tr in top_blocks(P[i], n) if tr] for i in range(N)]; NB = [[t for t, tr in top_blocks(P[i], n) if not tr] for i in range(N)]
SUPP = [frozenset().union(*TB[i]) if TB[i] else frozenset() for i in range(N)]
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
cnt = 0
for a in range(N):
    for c in nb[a]:
        for b in nb[c]:
            for d in nb[b]:
                if len({a,c,b,d}) < 4: continue
                xs = ar[comm[ar, a] & (th(c, ar) == th(d, ar)) & le[ar, a]]
                if not len(xs): continue
                # a-block meeting two T(d)-blocks, both inside supp b
                bad = [Z for Z in TB[a] + NB[a] if sum(1 for D in TB[d] if Z & D & SUPP[b]) >= 2]
                if bad:
                    cnt += 1
                    if cnt <= 3:
                        print('---')
                        for nm, i in zip('acbd', (a, c, b, d)): print(f"  {nm} = {show(i)}")
                        print("  u in:", '; '.join(show(i) for i in xs))
print("count", cnt)
