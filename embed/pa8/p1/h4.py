import pickle, numpy as np, sys
from collections import Counter
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed'); sys.path.insert(0, '/home/claude/pa8w/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n = int(sys.argv[1]); P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
R = np.concatenate([pickle.load(open(f, 'rb')) for f in sys.argv[2:]])
fails = Counter(); ex = {}; tot = 0
def check(name, cond, s):
    if not cond: fails[name] += 1; ex.setdefault(name, s)
def classes_via(blocks, links):
    """connected components of 'blocks' where two blocks are linked if they meet a common block in 'links'"""
    parent = list(range(len(blocks)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for L in links:
        idx = [i for i, Z in enumerate(blocks) if Z & L]
        for i in idx[1:]: parent[find(i)] = find(idx[0])
    comp = {}
    for i in range(len(blocks)): comp.setdefault(find(i), []).append(blocks[i])
    return list(comp.values())
for row in R:
    if len(set(row[:4])) < 4: continue
    a, c, b, d, x = [P[i] for i in row]; s = (a, c, b, d, x); tot += 1
    Tb = lambda p: [t for t, tr in top_blocks(p, n) if tr]; Nb = lambda p: [t for t, tr in top_blocks(p, n) if not tr]
    A, D = Tb(a), Tb(d); dbl = [t for t, tr in top_blocks(d, n)]; abl = [t for t, tr in top_blocks(a, n)]
    for comp in classes_via(dbl, Nb(a)):
        met = {Ai for Z in comp for Ai in A if Ai & Z}
        check('T7: d-blocks linked via N(a)-blocks meet ≤1 A', len(met) <= 1, s)
    for comp in classes_via(abl, Nb(d)):
        met = {Di for Y in comp for Di in D if Di & Y}
        check("T7': a-blocks linked via N(d)-blocks meet ≤1 D", len(met) <= 1, s)
print("instances:", tot)
for k, v in sorted(fails.items()): print(f"{v:5d} fail: {k}")
pickle.dump(ex, open('h4_ex.pkl', 'wb'))
