"""Explicit embeddings (SAT) of the maximal subalgebras of P^ch_n (family.py) and P^{R'}_n (rpfam.py), printed as block structures."""
import sys, os, json, time
os.environ['EMBED_DIR']='/home/claude/pa8w/embed'
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/wn'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/impl/rp2')
from pa_sat import solve
fam = sys.argv[1]; n = int(sys.argv[2]); mmax = int(sys.argv[3]) if len(sys.argv) > 3 else 8
if fam == 'ch':
    from family import build
else:
    from rpfam import build
T, names = build(n); N = len(T)
def gen(S):
    S = set(S); ch = True
    while ch:
        ch = False
        for x in list(S):
            for y in list(S):
                if T[x][y] not in S: S.add(T[x][y]); ch = True
    return S
irr = [x for x in range(N) if x not in gen(set(range(N)) - {x})]
print(f"{fam} n={n}: order {N}, irreducible {[names[i] for i in irr]}", flush=True)
for x in irr:
    S = sorted(gen(set(range(N)) - {x})); idx = {e: i for i, e in enumerate(S)}
    sub = [[idx[T[e][f]] for f in S] for e in S]
    for m in range(3, mmax + 1):
        t = time.time(); r = solve(sub, m, verbose=False)
        if r:
            print(f"omit {names[x]}: embeds in P(P_{m}) ({time.time()-t:.0f}s)")
            for e, blocks in zip(S, r):
                print(f"   {names[e]:4s} " + '  '.join(('[' if k == 'T' else '(') + ' '.join(map(str, b)) + (']' if k == 'T' else ')') for b, k in blocks))
            break
    sys.stdout.flush()
