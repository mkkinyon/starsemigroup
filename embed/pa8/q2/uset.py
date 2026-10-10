import pickle, numpy as np, sys, itertools
sys.path.insert(0, '/home/claude/pa8w/rp')
from blocks import top_blocks
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb')); N = len(P); ar = np.arange(N)
idx = {frozenset(frozenset(b) for b in p): i for i, p in enumerate(P)}
th = lambda x, p: T[p, x]; le = (T == ar[:, None])
def groups_of(a, u):
    A = [frozenset(j for j in blk if j < n) for blk in P[a] if any(j < n for j in blk) and any(j >= n for j in blk)]
    gr = []
    for blk in P[u]:
        top = frozenset(j for j in blk if j < n)
        if not top or not top <= frozenset().union(*A): continue
        tr = any(j >= n for j in blk)
        gr.append((frozenset(i for i, Ai in enumerate(A) if Ai <= top), tr))
    return A, gr
def make_u(a, A, gr):
    blocks = []
    for blk in P[a]:
        top = frozenset(j for j in blk if j < n)
        if not top: continue
        if not any(j >= n for j in blk): blocks.append(top); blocks.append(frozenset(j + n for j in top)); continue
    for (g, tr) in gr:
        top = frozenset().union(*[A[i] for i in g])
        if tr: blocks.append(top | frozenset(j + n for j in top))
        else: blocks.append(top); blocks.append(frozenset(j + n for j in top))
    return idx[frozenset(blocks)]
stats = {}
for a, c, b, d, us, ys in pickle.load(open(sys.argv[2], 'rb')):
    if len({a,c,b,d}) < 4: continue
    valid = lambda w: bool(th(c, w) == th(d, w))
    for u in us:
        A, gr = groups_of(a, u)
        # relabel one T group to N
        for j, (g, tr) in enumerate(gr):
            if tr:
                gr2 = gr[:j] + [(g, False)] + gr[j+1:]; k = ('T->N one group', valid(make_u(a, A, gr2))); stats[k] = stats.get(k, 0) + 1
            else:
                gr2 = gr[:j] + [(g, True)] + gr[j+1:]; k = ('N->T one group', valid(make_u(a, A, gr2))); stats[k] = stats.get(k, 0) + 1
        # merge two groups (label T if both T? try both labels)
        for j1, j2 in itertools.combinations(range(len(gr)), 2):
            g = gr[j1][0] | gr[j2][0]
            for lab in (True, False):
                gr2 = [x for j, x in enumerate(gr) if j not in (j1, j2)] + [(g, lab)]
                k = ('merge', 'labels', gr[j1][1], gr[j2][1], '->', lab, valid(make_u(a, A, gr2))); stats[k] = stats.get(k, 0) + 1
        # split a group of size>=2 into two parts (same label)
        for j, (g, tr) in enumerate(gr):
            if len(g) >= 2:
                gl = sorted(g)
                for r in range(1, len(gl)):
                    for part in itertools.combinations(gl, r):
                        g1 = frozenset(part); g2 = g - g1
                        gr2 = gr[:j] + [(g1, tr), (g2, tr)] + gr[j+1:]
                        k = ('split', tr, valid(make_u(a, A, gr2))); stats[k] = stats.get(k, 0) + 1
for k in sorted(stats, key=str): print(stats[k], k)
