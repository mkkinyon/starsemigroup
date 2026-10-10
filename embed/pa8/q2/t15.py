from hq import *
import pickle
n = 5; P, T = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
shown = 0; stats = {}
for f in ['instQ5_0.pkl', 'instQ5_1.pkl']:
  for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
    if len({a, c, b, d}) < 4: continue
    for u in us:
      for y in ys:
        s = structure(P, n, a, c, b, d, u, y)
        for E in s.Nc:
            if E not in s.Nd: continue
            dm = [m for m, (A, C, B, D) in enumerate(s.match) if C <= cls(E, s.Delta)]
            lk = [k for k, (A, C, B, D) in enumerate(s.match) if D <= cls(E, s.Lam)]
            if dm and lk and dm != lk:
                m, k = dm[0], lk[0]
                # which u-groups are m, k in? labels? does E meet supp y? is B_m in T-lab y-group? B_k?
                gm = next((lab, len(idx)) for idx, lab, AG, CG in s.groups if m in idx); gk = next((lab, len(idx)) for idx, lab, AG, CG in s.groups if k in idx)
                same = any(m in idx and k in idx for idx, lab, AG, CG in s.groups)
                key = ('same u-group', same, 'grp m', gm, 'grp k', gk, 'E meets supp y', bool(E & s.sy), 'B_m in supp y', bool(s.match[m][2] & s.sy), 'B_k in supp y', bool(s.match[k][2] & s.sy))
                stats[key] = stats.get(key, 0) + 1
                if shown < 3:
                    shown += 1; print('--- E =', sorted(E), 'Delta index', m, 'Lam index', k, key)
                    for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
                    print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match])
                    print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam), "| Pi1:", J(s.Pi1), "| Pi^a:", J(s.Pa), "| Pi^b:", J(s.Pb))
for k in sorted(stats, key=str): print(stats[k], k)
