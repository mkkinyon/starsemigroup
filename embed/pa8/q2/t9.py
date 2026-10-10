from hq import *
import pickle, sys
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
stats = {}; ex = {}
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
      for y in ys:
        s = structure(P, n, a, c, b, d, u, y)
        for (idx, lab, AG, CG) in s.groups:
            if not lab or len(idx) < 2: continue
            GG = cls(CG, s.Pi1)
            Diag = frozenset().union(*[s.match[i][1] & s.match[i][3] & s.sb for i in idx])
            Off = CG - Diag
            types = []
            for i in idx:
                Ai = s.match[i][0]
                t = 'b' if (Ai & CG) <= Diag else 'N'
                if not (Ai & CG): t += '0'
                types.append(t)
            # kappa structure: N(a)-blocks in Gamma_G: b-type or N(b)-type, which D they meet
            Fs = [F for F in s.Na if F <= GG]
            ftypes = tuple(sorted(('Nb' if F in s.Nb else 'b') + ('+D' if any(F & D for D in s.D) else '') for F in Fs))
            key = (tuple(sorted(types)), ftypes)
            stats[key] = stats.get(key, 0) + 1
            if key not in ex: ex[key] = (a, c, b, d, u, y, idx)
for key in sorted(stats, key=lambda k: -stats[k]): print(stats[key], key)
for key in list(ex)[:0]: pass
# show examples for keys with an N-type A and Nb N(a)-blocks meeting D
shown = 0
for key, (a, c, b, d, u, y, idx) in ex.items():
    if any(t.startswith('N') and not t.endswith('0') for t in key[0]) and any(ft == 'Nb+D' for ft in key[1]):
        s = structure(P, n, a, c, b, d, u, y)
        print('---', key, 'group', sorted(idx))
        for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
        print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match])
        print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam), "| Pi^a:", J(s.Pa), "| Pi^b:", J(s.Pb), "| K(y,c):", J(s.Kc))
        shown += 1
        if shown >= 4: break
