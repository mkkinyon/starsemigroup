"""Minimal non-embeddable projection algebras of order n+1 satisfying (Q1), from the embeddable algebras of order n.

A minimal non-embeddable algebra P of order n+1 has all proper subalgebras embeddable; deleting a maximal element e
gives an embeddable subalgebra of order n (Lemma: P \\ {e} is a subalgebra), so P is a one-point extension, by a new
maximal element, of an embeddable algebra of order n, subject to the axioms and (Q1) only (not (S), (R)).
This script enumerates these extensions with Mace4, and classifies them:
  * satisfying (S) and (R): they belong to the (Q1)+(S)+(R) census ord<n+1>.json, whose non-embeddable members are
    known (none for n+1 <= 6; P_7 for 7; the seven P_8^k for 8);
  * violating (S) or (R): non-embeddable; minimal iff no proper subalgebra is isomorphic to a known non-embeddable
    algebra of smaller order (P of order 6, P_7 of order 7), given the result for the smaller orders.
Usage: python3 q1ext.py n   (reads ord<n>.json = embeddable algebras of order n for n <= 7; writes q1ext<n+1>.json/.log)
Table convention: B[x][y] = x*y = theta_y(x)."""
import sys, os, json, subprocess, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); EMBED = os.path.dirname(HERE)
sys.path.insert(0, EMBED)
from mace4parse import parse_models
from layered_search import canon

AX = """op(400, infix, "*").
formulas(assumptions).
x * x = x.
(y * x) * x = y * x.
(x * y) * x = y * x.
((z * x) * y) * x = z * (y * x).
(((z * x) * y) * x) * y = (z * x) * y.
z * x != z | z * y != z | x * y = y * x.
"""
def extensions(B, workdir, tag):
    n = len(B); e = n
    inp = f"assign(domain_size, {n+1}).\nassign(max_models, -1).\nassign(max_seconds, -1).\n" + AX
    inp += f"{e} * x != {e} | x = {e}.\n"
    for x in range(n):
        for y in range(n): inp += f"{x} * {y} = {B[x][y]}.\n"
    inp += "end_of_list.\n"
    fin = os.path.join(workdir, f"q1ext_{tag}.in"); open(fin, "w").write(inp)
    env = dict(os.environ, PATH="/home/claude/bin:" + os.environ.get("PATH", ""))
    p = subprocess.run(f"mace4 -b 2000 -f {fin} 2>/dev/null | interpformat standard | isofilter 2>/dev/null",
                       shell=True, capture_output=True, text=True, env=env)
    os.remove(fin)
    return [T for N, T, c in parse_models(p.stdout)]

def th(B, p, q): return B[q][p]          # theta_p(q)
def mt(B, p, q): return th(B, p, q) == p and th(B, q, p) == q
def comm(B, p, q): return th(B, p, q) == th(B, q, p)
def holds_S(B):
    N = len(B); R = range(N)
    for a in R:
        for c in R:
            if not mt(B, a, c): continue
            for b in R:
                if not mt(B, b, c): continue
                for d in R:
                    if not mt(B, b, d) or not comm(B, c, d): continue
                    cd = th(B, c, d)
                    if th(B, a, cd) == th(B, b, cd) and not mt(B, a, d): return False
    return True
def holds_R(B):
    N = len(B); R = range(N)
    for a in R:
        for c in R:
            if not mt(B, a, c): continue
            for b in R:
                if not mt(B, b, c): continue
                for x in R:
                    if comm(B, x, a) and comm(B, x, c) and th(B, x, b) == th(B, x, c) and not mt(B, a, b): return False
    return True
def subalgebra_closed(B, S):
    return all(B[x][y] in S for x in S for y in S)
def restrict(B, S):
    S = sorted(S); idx = {s: i for i, s in enumerate(S)}
    return [[idx[B[x][y]] for y in S] for x in S]

# known minimal non-embeddable algebras of order <= 7 (theta tables, rows p columns q entry theta_p(q); converted)
def from_theta(names, TH):
    idx = {v: i for i, v in enumerate(names)}
    return [[idx[TH[y][x]] for y in names] for x in names]  # B[x][y] = theta_y(x) = TH[y][x]
Pnames = ['a', 'c', 'b', 'd', 'w', 'z']
PTH = {'a': dict(a='a', c='a', b='w', d='w', w='w', z='w'), 'c': dict(a='c', c='c', b='c', d='z', w='z', z='z'),
       'b': dict(a='w', c='b', b='b', d='b', w='w', z='w'), 'd': dict(a='z', c='z', b='d', d='d', w='z', z='z'),
       'w': {k: 'w' for k in Pnames}, 'z': {k: 'z' for k in Pnames}}
P6 = from_theta(Pnames, PTH)
P7names = ['a', 'c', 'b', 'x', 'u', 'v', 'w']
rows = {'a': 'a a u u u u u', 'c': 'c c c v v v v', 'b': 'w b b w w w w', 'x': 'u v v x u v v',
        'u': 'u u u u u u u', 'v': 'v v v v v v v', 'w': 'w w w w w w w'}
P7TH = {p: dict(zip(P7names, rows[p].split())) for p in P7names}
P7 = from_theta(P7names, P7TH)
KNOWN = {6: [canon(P6)], 7: [canon(P7)]}
assert holds_S(P7) and not holds_R(P7) and not holds_S(P6) and holds_R(P6)

def contains_known(B):
    N = len(B)
    for k, cans in KNOWN.items():
        if k >= N: continue
        for S in itertools.combinations(range(N), k):
            if subalgebra_closed(B, S) and canon(restrict(B, S)) in cans: return (k, S)
    return None

if __name__ == '__main__':
    n = int(sys.argv[1])
    if n == 8:   # bases = the embeddable algebras of order 8; known minimal non-embeddable of order 8 = the seven
        recs = [json.loads(l) for l in open(os.path.join(HERE, "post8.log"))]
        bases = [r["A"] for r in recs if r["embeds"] is not None]
        KNOWN[8] = [canon(r["A"]) for r in recs if r["embeds"] is None]
        assert len(KNOWN[8]) == 7 and len(bases) == 10821
    else:
        bases = json.load(open(os.path.join(HERE, f"ord{n}.json")))
    log = open(os.path.join(HERE, f"q1ext{n+1}.log"), "w"); t0 = time.time()
    seen = {}; nlab = 0
    for i, B in enumerate(bases):
        for T in extensions(B, HERE, f"{n}_{i}"):
            nlab += 1; key = canon(T)
            if key not in seen: seen[key] = (i, T)
        if i % 100 == 0: print(f"base {i}/{len(bases)}: {nlab} labelled, {len(seen)} distinct ({time.time()-t0:.0f}s)", file=log, flush=True)
    print(f"order {n+1}: {nlab} labelled extensions, {len(seen)} up to isomorphism ({time.time()-t0:.0f}s)", file=log, flush=True)
    census = set(canon(T) for T in json.load(open(os.path.join(HERE, f"ord{n+1}.json"))))
    nSR = 0; bad = []
    nonemb_census = []
    for key, (i, T) in seen.items():
        if holds_S(T) and holds_R(T):
            nSR += 1; assert key in census
            if n == 8 and contains_known(T) is None: nonemb_census.append((i, T))
        else:
            bad.append((i, T, contains_known(T)))
    print(f"satisfying (S),(R): {nSR} (all in ord{n+1}.json: {nSR == len(census)}); violating (S) or (R): {len(bad)}", file=log, flush=True)
    minimal = [(i, T) for i, T, c in bad if c is None]
    print(f"of these, containing a known non-embeddable proper subalgebra: {len(bad)-len(minimal)}; minimal non-embeddable: {len(minimal)}", file=log, flush=True)
    for i, T in minimal:
        print(f"  base {i}: S={holds_S(T)} R={holds_R(T)} table={T}", file=log, flush=True)
    if n == 8:
        print(f"(Q1)+(S)+(R) algebras of order 9 containing none of the nine known minimal ones: {len(nonemb_census)} (to be compared with the census of order 9)", file=log, flush=True)
        json.dump([T for i, T in nonemb_census], open(os.path.join(HERE, "q1ext9_SR_free.json"), "w"))
    json.dump({'distinct': len(seen), 'labelled': nlab, 'nSR': nSR, 'violating': len(bad), 'minimal': [T for i, T in minimal]},
              open(os.path.join(HERE, f"q1ext{n+1}.json"), "w"))
    print("done", file=log, flush=True)
