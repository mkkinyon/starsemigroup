import sys, pickle
from collections import Counter
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
cnt = Counter(); exs = {}
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y)
    GammaA = {G for (_, _, _, G, _) in s.match}; DeltaB = {D for (_, _, _, _, D) in s.match}
    Ntil = set(s.Ntil)
    for E in s.Nc:
        loc = 'suppx' if E <= s.sx else ('Ntil' if E in Ntil else ('Y' if not (E & s.sy) else 'mixed'))
        G = next(G for G in s.Gamma if E <= G); D = next(D for D in s.Delta if E <= D)
        isNa = E in s.Na
        key = ('N(c)', loc, 'GammaA' if G in GammaA else 'Gamma0', 'DeltaB' if D in DeltaB else 'Delta0', 'alsoN(a)' if isNa else '')
        cnt[key] += 1
        if key not in exs: exs[key] = (a, c, b, x, y)
for k, v in sorted(cnt.items()): print(f"{v:7d} {k}")
pickle.dump(exs, open('harness6_ex.pkl', 'wb'))
