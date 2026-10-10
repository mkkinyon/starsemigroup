from hq import *
import pickle
P, T = pickle.load(open('/home/claude/pa8w/gen/tab4.pkl', 'rb')); n = 4
shown = 0
for a, c, b, d, us, ys in pickle.load(open('instQ4.pkl', 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
        s = structure(P, n, a, c, b, d, u, y=ys[0])
        bad = [(idx, lab) for (idx, lab, AG, CG) in s.groups if lab and not all(s.match[i][3] <= cls(s.match[i][0], s.rho) for i in idx)]
        if bad:
            print('---', 'groups:', [(sorted(idx), 'T' if lab else 'N') for idx, lab, _, _ in s.groups])
            for nm, i in zip('acbdu', (a, c, b, d, u)): print(f"  {nm} = {show(P, n, i)}")
            print("  y in:", '; '.join(show(P, n, i) for i in ys))
            print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in m) for m in s.match])
            print("  rho:", [sorted(K) for K in s.rho], " Pi1:", [sorted(K) for K in s.Pi1])
            shown += 1
    if shown >= 3: break
