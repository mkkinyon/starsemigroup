"""Referee's dropped-hypothesis map for the K0 proof, P_4 (own generator, own claim checker k0claims_ref.check).
Columns: full; -H1 (yc=cy); -H2 (th_y(b)=v); -H3 (th_b(z)=b); -H4 (th_z(a)=th_z(b)); -H4+th_a(z)=a; -H5 (th_y(z)=u).
a><c><b is always kept.  Usage: python3 k0drop_ref.py [n]
"""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/review4/review-scripts')
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import projections, theta, commute, matched
from k0claims_ref import check

n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
P = projections(n); idx = {p: i for i, p in enumerate(P)}; NP = len(P)
t0 = time.time()
TH = [[idx[theta(p, q)] for q in P] for p in P]
CM = [[commute(p, q) for q in P] for p in P]
MT = [[TH[i][j] == i and TH[j][i] == j for j in range(NP)] for i in range(NP)]
print('P_%d: %d projections, tables in %.0fs' % (n, NP, time.time() - t0), flush=True)

COLS = ['full', '-H1 yc=cy', '-H2 th_y(b)=v', '-H3 th_b(z)=b', '-H4 th_z(a)=th_z(b)', '-H4 +th_a(z)=a', '-H5 th_y(z)=u']
fails = {}; counts = {c: 0 for c in COLS}

def tally(col, inst):
    counts[col] += 1
    R = check(inst)
    for k, v in R.items():
        d = fails.setdefault(k, {c: 0 for c in COLS})
        if '(info)' in k:
            if v: d[col] += 1
        elif not v: d[col] += 1

for ai in range(NP):
    for ci in range(NP):
        if not MT[ai][ci]: continue
        Yc = [yi for yi in range(NP) if CM[yi][ci]]
        for bi in range(NP):
            if not MT[ci][bi]: continue
            u = TH[ai][bi]; v = TH[bi][ai]
            Y12 = [yi for yi in Yc if TH[yi][bi] == v]
            Y1 = Yc                                                 # -H2
            Y2 = [yi for yi in range(NP) if TH[yi][bi] == v]        # -H1
            Z34 = [zi for zi in range(NP) if TH[bi][zi] == bi and TH[zi][ai] == TH[zi][bi]]
            Z3 = [zi for zi in range(NP) if TH[bi][zi] == bi]      # -H4
            Z3a = [zi for zi in Z3 if TH[ai][zi] == ai]            # -H4 + th_a(z)=a
            Z4 = [zi for zi in range(NP) if TH[zi][ai] == TH[zi][bi]]  # -H3
            def mk(yi, zi): return {'a': P[ai], 'b': P[bi], 'c': P[ci], 'y': P[yi], 'z': P[zi]}
            for yi in Y12:
                for zi in Z34:
                    tally('-H5 th_y(z)=u', mk(yi, zi))
                    if TH[yi][zi] == u: tally('full', mk(yi, zi))
                for zi in Z4:
                    if TH[yi][zi] == u: tally('-H3 th_b(z)=b', mk(yi, zi))
                for zi in Z3:
                    if TH[yi][zi] == u:
                        tally('-H4 th_z(a)=th_z(b)', mk(yi, zi))
                        if TH[ai][zi] == ai: tally('-H4 +th_a(z)=a', mk(yi, zi))
            for yi in Y1:
                for zi in Z34:
                    if TH[yi][zi] == u: tally('-H2 th_y(b)=v', mk(yi, zi))
            for yi in Y2:
                for zi in Z34:
                    if TH[yi][zi] == u: tally('-H1 yc=cy', mk(yi, zi))
    if ai % 10 == 9: print('  a-index %d/%d, %.0fs' % (ai + 1, NP, time.time() - t0), flush=True)

print('P_%d dropped-hypothesis map (%.0fs). Entries: FAILS/instances; (info) rows: holds/instances' % (n, time.time() - t0))
print('%-70s' % 'statement' + ''.join('%20s' % c for c in COLS))
print('%-70s' % 'instances' + ''.join('%20d' % counts[c] for c in COLS))
for k, d in fails.items():
    print('%-70s' % k + ''.join('%20s' % ('%d/%d' % (d[c], counts[c])) for c in COLS))
