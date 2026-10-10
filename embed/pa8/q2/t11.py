from hq import *
import pickle, sys
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
shown = 0
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
      for y in ys:
        s = structure(P, n, a, c, b, d, u, y)
        for (idx, lab, AG, CG) in s.groups:
            if not lab or len(idx) < 2: continue
            GG = cls(CG, s.Pi1)
            NN = [E for E in s.Nc if E in s.Nd and E <= GG]
            if not NN: continue
            found = False
            for m in idx:
                Am, Cm, Bm, Dm = s.match[m]
                offk = [k for k in idx if k != m and (Am & s.match[k][3])]
                if not offk: continue
                Fs = [F for F in s.Na if F & Cm & Dm]
                if Fs: found = True
            if found:
                print('--- group', sorted(idx))
                for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
                print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match])
                print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam), "| Pi^a:", J(s.Pa), "| Pi^b:", J(s.Pb), "| K(y,c):", J(s.Kc))
                shown += 1
        if shown >= 3: break
      if shown >= 3: break
    if shown >= 3: break
  if shown >= 3: break
print("shown", shown)
