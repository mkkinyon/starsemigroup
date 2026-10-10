from hq import *
import pickle
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
shown = 0; seen = set()
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4 or (a, c, b, d) in seen: continue
    for u in us:
        s = structure(P, n, a, c, b, d, u, ys[0])
        hubs = [(idx, CG) for idx, lab, AG, CG in s.groups if CG in s.Nd and len(idx) == 2]
        if not hubs: continue
        seen.add((a, c, b, d))
        idx, CG = hubs[0]; GG = cls(CG, s.Pi1); E = GG & s.sd
        print('--- hub group', sorted(idx), 'C_G =', sorted(CG), 'E_G =', sorted(E))
        for nm, i in zip('acbdu', (a, c, b, d, u)): print(f"  {nm} = {show(P, n, i)}")
        print("  y in:", '; '.join(show(P, n, i) for i in ys[:5]))
        print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match])
        print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam), "| Pi1:", J(s.Pi1))
        shown += 1; break
    if shown >= 5: break
  if shown >= 5: break
