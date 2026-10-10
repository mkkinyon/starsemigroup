import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks, join_classes
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
th = lambda x, p: T[p, x]; comm = (T == T.T)
R = pickle.load(open('/home/claude/pa8w/q/instQ4.pkl', 'rb')); a, c, b, d, x, y = R.T
nc = ~comm[a, b]; print("instances with ab != ba:", nc.sum(), " of", len(R))
def show(i): return ' '.join(('T' if tr else 'N') + ''.join(map(str, sorted(t))) for t, tr in top_blocks(P[i], n))
# distinct (a,c,b,d,y) with ab != ba, sorted by rank of y desc; show a few paths with all their y's
from collections import defaultdict
ys = defaultdict(set)
for row in R[nc]: ys[tuple(row[:4])].add(row[5])
print("paths with ab!=ba:", len(ys))
rk = lambda i: sum(tr for _, tr in top_blocks(P[i], n))
shown = 0
for path, yy in ys.items():
    if len(set(path)) < 4: continue
    print("---"); 
    for nm, i in zip('acbd', path): print(f"  {nm} = {show(i)}")
    print("  y in:", '; '.join(show(i) for i in sorted(yy, key=rk)))
    shown += 1
    if shown >= 6: break
