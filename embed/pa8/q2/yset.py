import pickle, numpy as np, sys, itertools
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
idx = {frozenset(frozenset(b) for b in p): i for i, p in enumerate(P)}
th = lambda x, p: T[p, x]; comm = (T == T.T)
def blocks_of(y):
    out = []
    for blk in P[y]:
        top = frozenset(j for j in blk if j < n)
        if top: out.append((top, any(j >= n for j in blk)))
    return out
def make(bl):
    blocks = []
    for top, tr in bl:
        if tr: blocks.append(top | frozenset(j + n for j in top))
        else: blocks.append(top); blocks.append(frozenset(j + n for j in top))
    return idx[frozenset(blocks)]
stats = {}
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    valid = lambda w: bool(comm[w, a] and comm[w, b] and th(w, c) == th(w, b))
    for y in ys:
        bl = blocks_of(y)
        for j, (top, tr) in enumerate(bl):
            bl2 = bl[:j] + [(top, not tr)] + bl[j+1:]
            k = ('relabel one block', 'T->N' if tr else 'N->T', valid(make(bl2))); stats[k] = stats.get(k, 0) + 1
        for j1, j2 in itertools.combinations(range(len(bl)), 2):
            for lab in (True, False):
                bl2 = [x for j, x in enumerate(bl) if j not in (j1, j2)] + [(bl[j1][0] | bl[j2][0], lab)]
                k = ('merge', bl[j1][1], bl[j2][1], '->', lab, valid(make(bl2))); stats[k] = stats.get(k, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
