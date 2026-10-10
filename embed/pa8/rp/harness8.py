import sys, pickle
from collections import Counter
exec(open('harness.py').read().split("fails = {}; ex = {}; count = 0")[0])
cnt = Counter(); exs = {}
for a, c, b, x, y in inst:
    if a == c: continue
    x = m(x, y)
    s = structure(a, c, b, x, y)
    GammaA = {G: i for i, (_, _, _, G, _) in enumerate(s.match)}; DeltaB = {D: i for i, (_, _, _, _, D) in enumerate(s.match)}
    Ntil = set(s.Ntil)
    cblocks = [t for t, tr in top_blocks(c, n)]
    def loc(E):
        if E in s.C: return 'C'
        return 'suppx' if E <= s.sx else ('Ntil' if E in Ntil else 'Y')
    Gof = {E: next(G for G in s.Gamma if E <= G) for E in cblocks}
    Dof = {E: next(D for D in s.Delta if E <= D) for E in cblocks}
    # for each B-free Delta class F containing an Ntil of some Gamma_i: profile of its c-blocks
    for F in s.Delta:
        if F in DeltaB: continue
        Es = [E for E in cblocks if Dof[E] == F]
        gis = {GammaA[Gof[E]] for E in Es if Gof[E] in GammaA}
        if not gis: continue
        prof = tuple(sorted(Counter((loc(E), 'GammaA' if Gof[E] in GammaA else 'Gamma0') for E in Es).items()))
        key = ('F with Gamma_i-blocks', f'#distinct i={len(gis)}', prof)
        cnt[key] += 1
        if key not in exs: exs[key] = (a, c, b, x, y)
        # the A-free Gamma classes G adjacent to F: which Delta classes do they touch?
        for E in Es:
            G = Gof[E]
            if G in GammaA: continue
            Ds = {Dof[E2] for E2 in cblocks if Gof[E2] == G}
            key2 = ('A-free G adjacent to such F touches', f'DeltaB={sum(1 for D in Ds if D in DeltaB)}', f'other B-free={sum(1 for D in Ds if D not in DeltaB and D != F)}')
            cnt[key2] += 1
            if key2 not in exs: exs[key2] = (a, c, b, x, y)
    # for Delta_i: the A-free Gamma classes it touches: what other Delta classes do they touch?
    for D, i in DeltaB.items():
        Es = [E for E in cblocks if Dof[E] == D]
        for E in Es:
            G = Gof[E]
            if G in GammaA: continue
            Ds = {Dof[E2] for E2 in cblocks if Gof[E2] == G}
            key3 = ('A-free G adjacent to Delta_i touches', f'other DeltaB={sum(1 for D2 in Ds if D2 in DeltaB and D2 != D)}', f'B-free={sum(1 for D2 in Ds if D2 not in DeltaB)}', loc(E))
            cnt[key3] += 1
            if key3 not in exs: exs[key3] = (a, c, b, x, y)
for k, v in sorted(cnt.items()): print(f"{v:7d} {k}")
pickle.dump(exs, open('harness8_ex.pkl', 'wb'))
