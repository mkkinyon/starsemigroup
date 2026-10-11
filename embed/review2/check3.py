"""Verify Prop 5.37 embeddings with the reviewer's theta (Lemma 1.1(a)); block lists taken from chemb/rpemb.make."""
import sys
sys.path.insert(0, '/home/claude/pa8w/review2/code')
from blk import proj, theta, show
from check2 import Pch, PRp, table
import chemb, rpemb

def run(fam, mk, maker, nmax):
    for n in range(1, nmax + 1):
        els, th = fam(n); T = table(els, th)
        omits = ['a', 'c', 'b'] + (list(range(1, n + 1)) if mk == 'ch' else ['k'] + list(range(1, n)))
        for om in omits:
            name_om = f'x{om}' if isinstance(om, int) else om
            pts, E = maker(n, om)
            P = {}
            for e, bl in E.items():
                P[e] = proj([b for b, _ in bl], [b for b, kd in bl if kd == 'T'])
            S = [e for e in els if e != name_om]
            assert set(S) == set(P)
            assert len(set(P.values())) == len(P)
            bad = []
            for x in S:
                for y in S:
                    want = th(y, x)   # theta_y(x)
                    assert want in S, (x, y, want)
                    if theta(P[y], P[x]) != P[want]: bad.append((x, y, want))
            print(f'{mk} n={n} omit {name_om}: m={len(pts)}, {len(bad)} wrong', bad[:3])

run(Pch, 'ch', chemb.make, 8)
run(PRp, 'rp', rpemb.make, 8)
