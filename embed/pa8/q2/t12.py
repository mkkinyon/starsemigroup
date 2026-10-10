from hq import *
import pickle, sys
n = int(sys.argv[1]) if __name__ == "__main__" else 4; files = sys.argv[2:]
P, T = pickle.load(open(f"/home/claude/pa8w/gen/tab{n}.pkl", "rb")) if __name__ == "__main__" else (None, None)
J = lambda cl: ' '.join(''.join(map(str, sorted(K))) for K in cl)
def kappas(s, GG):
    """components of the graph on N(a)-blocks in GG and N(c)∩N(d)-blocks in GG"""
    V = [F for F in s.Na if F <= GG] + [E for E in s.Nc if E in s.Nd and E <= GG]
    parent = list(range(len(V)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(V)):
        for j in range(i):
            if V[i] & V[j]: parent[find(i)] = find(j)
    comps = {}
    for i in range(len(V)): comps.setdefault(find(i), []).append(V[i])
    return list(comps.values())
if __name__ == '__main__':
    stats = {}; ex = {}
    
    for f in files:
      for a, c, b, d, us, ys in pickle.load(open(f, 'rb')):
        if len({a, c, b, d}) < 4: continue
        for u in us:
          for y in ys:
            s = structure(P, n, a, c, b, d, u, y)
            for (idx, lab, AG, CG) in s.groups:
                if not lab: continue
                GG = cls(CG, s.Pi1)
                for kap in kappas(s, GG):
                    alpha = [i for i in idx if any(E & s.match[i][0] for E in kap if E in s.Nc)]
                    Ds = [k for k in idx if any(F & s.match[k][3] for F in kap if F in s.Na)]
                    gam = [m for m in idx if any(E & s.match[m][1] for E in kap)]
                    key = ('alpha', len(alpha), 'nD', len(Ds), 'diag' if Ds and gam and Ds == gam else ('off' if Ds else '-'), 'ycase', 'rank0' if not s.Y else 'rank>0')
                    stats[key] = stats.get(key, 0) + 1
                    if key not in ex: ex[key] = (a, c, b, d, u, y, idx)
    for k in sorted(stats): print(stats[k], k)
    for key, (a, c, b, d, u, y, idx) in ex.items():
        if key[1] == 1 and key[3] == 1 and key[4] == 'off':
            s = structure(P, n, a, c, b, d, u, y); print('---', key, sorted(idx))
            for nm, i in zip('acbduy', (a, c, b, d, u, y)): print(f"  {nm} = {show(P, n, i)}")
            print("  match (A,C,B,D):", [tuple(''.join(map(str, sorted(t))) for t in mm) for mm in s.match])
            print("  rho:", J(s.rho), "| Gamma:", J(s.Gamma), "| Delta:", J(s.Delta), "| Lam:", J(s.Lam))
