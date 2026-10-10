import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
rows = pickle.load(open(sys.argv[2], 'rb'))
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
rk = lambda i: sum(tr for _, tr in top_blocks(P[i], n))
stats = {}; ex = []
for a, c, b, d, us, ys in rows:
    if len({a,c,b,d}) < 4: continue
    ys = list(ys)
    greatest = [y for y in ys if all(le[z, y] for z in ys)]
    maxrk = max(rk(y) for y in ys); nmax = sum(1 for y in ys if rk(y) == maxrk)
    k = ('greatest' if greatest else 'no greatest', 'unique maxrank' if nmax == 1 else 'several maxrank')
    stats[k] = stats.get(k, 0) + 1
    if not greatest and len(ex) < 3: ex.append((a, c, b, d, ys))
print(stats)
for a, c, b, d, ys in ex:
    print('---')
    for nm, i in zip('acbd', (a, c, b, d)): print(f"  {nm} = {show(i)}")
    print("  y in:", '; '.join(show(i) for i in sorted(ys, key=rk)))
