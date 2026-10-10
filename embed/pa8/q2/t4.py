from hq import *
import pickle, sys
n = int(sys.argv[1]); files = sys.argv[2:]
P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
def ygroups(s):
    """partition of T(a) by Pi^a classes, with labels: T if class meets supp y"""
    gr = []
    for K in s.Pa:
        idx = frozenset(i for i, (Ai, _, _, _) in enumerate(s.match) if Ai <= K)
        if idx: gr.append((idx, bool(K & s.sy)))
    return gr
shown = 0; stats = {}
for f in files:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
      for y in ys:
        s = structure(P, n, a, c, b, d, u, y)
        yg = ygroups(s)
        for (idx, lab, AG, CG) in s.groups:
            for (idy, laby) in yg:
                common = idx & idy
                if len(common) >= 2:
                    key = ('u' + ('T' if lab else 'N'), 'y' + ('T' if laby else 'N'), len(common)); stats[key] = stats.get(key, 0) + 1
                    if shown < 4 and len(common) == 2 and n == 5:
                        shown += 1
                        print('--- u-group', sorted(idx), 'T' if lab else 'N', ' y-group', sorted(idy), 'T' if laby else 'N')
                        for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
                        print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in m) for m in s.match])
                        print("  rho:", [sorted(K) for K in s.rho])
print(stats)
