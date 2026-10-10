from hq import *
import pickle, sys
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
rk = lambda i: sum(tr for _, tr in top_blocks(P[i], n))
shown = 0
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    y = max(ys, key=rk)
    if rk(y) == 0: continue
    for u in us:
        s = structure(P, n, a, c, b, d, u, y)
        big = [(idx, CG) for idx, lab, AG, CG in s.groups if lab and len(idx) >= 2]
        if not big: continue
        # want: some N(a)-block inside Gamma_G, and y with T-blocks meeting Gamma_G, and non-sigma matching
        idx, CG = big[0]; GG = cls(CG, s.Pi1)
        if not any(F <= GG for F in s.Na): continue
        if not any(Y & GG for Y in s.Y): continue
        if all(s.match[i][3] <= cls(s.match[i][0], s.rho) for i in idx): continue
        print('--- T-group', sorted(idx))
        for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
        print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in m) for m in s.match])
        J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
        print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam), "| Pi1:", J(s.Pi1))
        print("  Pi^a:", J(s.Pa), "| Pi^b:", J(s.Pb), "| K(y,c):", J(s.Kc), "| K(y,d):", J(s.Kd))
        shown += 1; break
    if shown >= 4: break
  if shown >= 4: break
