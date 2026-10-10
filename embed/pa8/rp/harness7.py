import sys, pickle
from collections import Counter
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
cnt = Counter(); exs = {}
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y)
    GammaA = {G for (_, _, _, G, _) in s.match}; DeltaB = {D for (_, _, _, _, D) in s.match}
    Ntil = set(s.Ntil); sv = frozenset().union(*s.V) if s.V else frozenset(); su = frozenset().union(*s.U) if s.U else frozenset()
    for E in s.Na:
        if E in s.Nc: continue  # common N-blocks: trivial
        loc = 'suppy' if E <= s.sy else ('Y' if not (E & s.sy) else 'mixed')
        G = next(G for G in s.Gamma if E <= G)
        dB = sum(1 for D in DeltaB if E & D); d0 = sum(1 for D in s.Delta if (E & D) and D not in DeltaB)
        sub = 'in V' if E <= sv else ('meets V' if E & sv else 'no V')
        key = ('N(a)', loc, 'GammaA' if G in GammaA else 'Gamma0', f'DeltaB met={dB}', f'Delta0 met={min(d0,2)}', sub, 'meets suppx' if E & s.sx else 'outside suppx')
        cnt[key] += 1
        if key not in exs: exs[key] = (a, c, b, x, y)
    for E in s.Nb:
        if E in s.Nc: continue
        loc = 'in Ntil' if any(E & N and (E & s.sy) <= N for N in Ntil) else ('Y' if not (E & s.sy) else ('in suppx' if (E & s.sy) <= s.sx else 'mixed'))
        D = next(D for D in s.Delta if E <= D)
        gA = sum(1 for G in GammaA if E & G); g0 = sum(1 for G in s.Gamma if (E & G) and G not in GammaA)
        key = ('N(b)', loc, 'DeltaB' if D in DeltaB else 'Delta0', f'GammaA met={gA}', f'Gamma0 met={min(g0,2)}', 'meets V' if E & sv else 'no V', 'meets U' if E & su else 'no U')
        cnt[key] += 1
        if key not in exs: exs[key] = (a, c, b, x, y)
for k, v in sorted(cnt.items()): print(f"{v:7d} {k}")
pickle.dump(exs, open('harness7_ex.pkl', 'wb'))
