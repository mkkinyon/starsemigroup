from hq import *
import pickle, sys
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
shown = 0
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
        s = structure(P, n, a, c, b, d, u, y=ys[0])
        if not all(len(idx) == 1 and not lab for idx, lab, _, _ in s.groups): continue
        hubs = [(idx, CG) for idx, lab, AG, CG in s.groups if CG in s.Nd]
        if not hubs: continue
        # nontrivial: some hub class Gamma_i contains an N(a)-block, and A_i does not meet E_i directly
        ok = False
        for idx, CG in hubs:
            i = next(iter(idx)); Ai = s.match[i][0]; GG = cls(CG, s.Pi1); E = GG & s.sd
            if E and not (Ai & E) and any(F <= GG for F in s.Na): ok = True
        if not ok: continue
        print('---', 'groups:', [(sorted(idx), 'T' if lab else 'N') for idx, lab, _, _ in s.groups], 'hubs:', [sorted(CG) for _, CG in hubs])
        for nm, i in zip('acbdu', (a, c, b, d, u)): print(f"  {nm} = {show(P, n, i)}")
        print("  y in:", '; '.join(show(P, n, i) for i in ys[:6]))
        print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in m) for m in s.match])
        print("  rho:", [sorted(K) for K in s.rho], " Gamma:", [sorted(K) for K in s.Gamma], " Delta:", [sorted(K) for K in s.Delta], " Lam:", [sorted(K) for K in s.Lam])
        shown += 1
        break
    if shown >= 4: break
  if shown >= 4: break
