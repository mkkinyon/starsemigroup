import pickle, numpy as np, sys
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
idx = {frozenset(frozenset(b) for b in p): i for i, p in enumerate(P)}
th = lambda x, p: T[p, x]; le = (T == ar[:, None])
def relabel_all(i, lab):
    blocks = []
    for blk in P[i]:
        top = frozenset(j for j in blk if j < n)
        if not top: continue
        if lab: blocks.append(top | frozenset(j + n for j in top))
        else: blocks.append(top); blocks.append(frozenset(j + n for j in top))
    return idx[frozenset(blocks)]
rows = pickle.load(open(sys.argv[2], 'rb')); stats = {}
for a, c, b, d, us, ys in rows:
    if len({a,c,b,d}) < 4: continue
    a0 = relabel_all(a, False); ok0 = th(c, a0) == th(d, a0)
    # finest u with u's labels: singleton groups, label of A_i = label of its u-group
    fine_ok = []
    for u in us:
        blocks = []
        for blk in P[u]:
            top = frozenset(j for j in blk if j < n)
            if not top: continue
            tr = any(j >= n for j in blk)
            # split top into a-blocks
            for ablk in P[a]:
                atop = frozenset(j for j in ablk if j < n)
                if atop and atop <= top:
                    if tr: blocks.append(atop | frozenset(j + n for j in atop))
                    else: blocks.append(atop); blocks.append(frozenset(j + n for j in atop))
        uf = idx[frozenset(blocks)]
        fine_ok.append(bool(th(c, uf) == th(d, uf)))
    k = ('a0 valid' if ok0 else 'a0 invalid', 'fine valid' if all(fine_ok) else 'fine invalid', 'a valid' if th(c, a) == th(d, a) else 'a invalid')
    stats[k] = stats.get(k, 0) + 1
print(stats)
