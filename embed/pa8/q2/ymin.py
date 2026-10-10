import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
th = lambda x, p: T[p, x]; comm = (T == T.T); le = (T == ar[:, None])
rows = pickle.load(open(sys.argv[2], 'rb'))
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
rk = lambda i: sum(tr for _, tr in top_blocks(P[i], n))
stats = {'least exists': 0, 'no least': 0, 'closed under th_y1(y2) if commute': 0, 'not closed': 0, 'min-rank unique': 0, 'min-rank not unique': 0, 'rank0 exists': 0}
ex = []
for a, c, b, d, us, ys in rows:
    if len({a, c, b, d}) < 4: continue
    ys = list(ys); S = set(ys)
    least = [y for y in ys if all(le[y, z] for z in ys)]
    stats['least exists' if least else 'no least'] += 1
    mr = min(rk(y) for y in ys); mins = [y for y in ys if rk(y) == mr]
    stats['min-rank unique' if len(mins) == 1 else 'min-rank not unique'] += 1
    if mr == 0: stats['rank0 exists'] += 1
    cl = all((not comm[y1, y2]) or (th(y1, y2) in S) for y1 in ys for y2 in ys)
    stats['closed under th_y1(y2) if commute' if cl else 'not closed'] += 1
    if not least and len(ex) < 3: ex.append((a, c, b, d, ys))
print(stats)
for a, c, b, d, ys in ex:
    print('---')
    for nm, i in zip('acbd', (a, c, b, d)): print(f"  {nm} = {show(i)}")
    print("  y in:", '; '.join(show(i) for i in sorted(ys, key=rk)))
