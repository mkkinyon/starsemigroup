import pickle, numpy as np, sys
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); N = len(P); ar = np.arange(N); n = 4
idx = {frozenset(frozenset(b) for b in p): i for i, p in enumerate(P)}
th = lambda x, p: T[p, x]
comm = (T == T.T)
R = pickle.load(open('/home/claude/pa8w/q/instQ4.pkl', 'rb')); a, c, b, d, x, y = R.T
def relabel(i, lab):
    blocks = []
    for blk in P[i]:
        top = frozenset(j for j in blk if j < n)
        if not top: continue
        blocks.append(top | frozenset(j + n for j in top) if lab else top)
        if not lab: blocks.append(frozenset(j + n for j in top))
    return idx[frozenset(blocks)]
# check P format
print(type(P[0]), list(P[0])[:3])
y0 = np.array([relabel(i, False) for i in range(N)]); y1 = np.array([relabel(i, True) for i in range(N)])
def hyp(yy): return comm[yy, a] & comm[yy, b] & (th(yy, c) == th(yy, b))
tests = {'y0 (all N)': hyp(y0[y]), 'y1 (all T)': hyp(y1[y]), 'th_b(th_a(y))': hyp(th(b, th(a, y))), 'th_a(th_b(y))': hyp(th(a, th(b, y))),
         'th_y(th_a(b))': hyp(th(y, th(a, b))), 'th_y(th_b(a))': hyp(th(y, th(b, a))), 'a': hyp(a), 'b': hyp(b), 'th_a(b)': hyp(th(a, b)), 'th_b(a)': hyp(th(b, a)),
         'th_y(c)': hyp(th(y, c)), 'th_c(y)': hyp(th(c, y)), 'th_y(a)': hyp(th(y,a)), 'th_y(b)': hyp(th(y,b))}
for k, v in tests.items(): print(f"{k:20s} fails {np.count_nonzero(~v)}")
# how often does the y-hypothesis hold for y=a? y=b? for the *path*: exists y among these canonical ones?
