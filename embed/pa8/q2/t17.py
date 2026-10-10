from hq import *
import pickle
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
stats = {}; shown = 0
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
      for y in ys:
        s = structure(P, n, a, c, b, d, u, y)
        for Z in s.A + s.Na:
            if Z not in s.Ny: continue
            Bs = [k for k, m in enumerate(s.match) if m[2] <= Z]
            if len(Bs) < 2 or frozenset().union(*[s.match[k][2] for k in Bs]) != Z: continue
            # Z is an N(y)-block that is a union of >= 2 T(b)-blocks
            Es = [E for E in s.Nc if E in s.Nd and E & Z]
            lam_idx = sorted({k for E in Es for k, m in enumerate(s.match) if m[3] <= cls(E, s.Lam)})
            key = ('Z is', 'T(a)' if Z in s.A else 'N(a)', '#B', len(Bs), 'meets #common N-blocks', len(Es), 'Lam indices of those', len(lam_idx), 'Z meets supp d', bool(Z & s.sd), 'Z meets supp c', bool(Z & s.sc))
            stats[key] = stats.get(key, 0) + 1
            if len(Es) >= 1 and shown < 3:
                shown += 1; print('--- Z =', sorted(Z), key)
                for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
                print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match])
                print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam), "| Pi1:", J(s.Pi1))
for k in sorted(stats, key=str): print(stats[k], k)
