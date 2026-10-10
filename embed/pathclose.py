"""Systematic search for 'path-closing' quasi-identities valid in P(P_m):
  hypotheses: a matched path p_0 ~ p_1 ~ ... ~ p_n  plus atomic relations between an auxiliary projection x and the
  vertices;  conclusion p_0 ~ p_n.
Atoms (for each vertex p, pair {p,q} of vertices):  comm(x,p);  x<=p;  p<=x;  sees(x;p,q): theta_x(p)=theta_x(q);
  seen(p,q;x): theta_p(x)=theta_q(x);  x=theta_p(q) (ordered pair).
For every instance of the path with p_0 not matched to p_n and every x, the set of atoms that hold is a
'counterexample signature'; a set H of atoms is a valid hypothesis set iff no signature contains it.  The minimal
valid sets (up to the given size) are printed; they are the candidate obstructions of this shape.
Usage: python3 pathclose.py m n [maxsize]"""
import sys, itertools
from pa_embed2 import PPm

def run(m, n, maxsize=4, verbose=True):
    D = PPm(m); N = D.N; tab = D.tab
    th = lambda p, q: tab[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    matched = {p: [q for q in range(N) if mt(p, q)] for p in range(N)}
    V = ['p%d' % i for i in range(n + 1)]     # vertex names p_0..p_n
    atoms = []
    for i in range(n + 1):
        atoms.append(('comm', i)); atoms.append(('xle', i)); atoms.append(('lex', i))
    for i, j in itertools.combinations(range(n + 1), 2):
        atoms.append(('sees', i, j)); atoms.append(('seen', i, j))
    for i in range(n + 1):
        for j in range(n + 1):
            if i != j: atoms.append(('xeq', i, j))
    def atom_holds(at, P, x):
        k = at[0]
        if k == 'comm': return th(x, P[at[1]]) == th(P[at[1]], x)
        if k == 'xle': return th(P[at[1]], x) == x
        if k == 'lex': return th(x, P[at[1]]) == P[at[1]]
        if k == 'sees': return th(x, P[at[1]]) == th(x, P[at[2]])
        if k == 'seen': return th(P[at[1]], x) == th(P[at[2]], x)
        if k == 'xeq': return th(P[at[1]], P[at[2]]) == x
    sigs = set(); ninst = 0
    def paths(prefix):
        if len(prefix) == n + 1:
            yield prefix; return
        for q in matched[prefix[-1]]:
            yield from paths(prefix + [q])
    pos = set()
    for p0 in range(N):
        for P in paths([p0]):
            if len(set(P)) < len(P): continue
            closed = mt(P[0], P[-1])
            for x in range(N):
                if x in P: continue
                sig = sum(1 << k for k, at in enumerate(atoms) if atom_holds(at, P, x))
                if closed: pos.add(sig)
                else: ninst += 1; sigs.add(sig)
    sigs = list(sigs)
    # remove non-maximal signatures (only maximal ones matter)
    sigs.sort(key=lambda s: -bin(s).count('1'))
    maxs = []
    for s in sigs:
        if not any((s & t) == s for t in maxs): maxs.append(s)
    if verbose:
        print(f"m={m}, n={n}: {ninst} instances with p_0 !~ p_n (distinct vertices, x not a vertex), {len(sigs)} signatures, {len(maxs)} maximal", flush=True)
        for s_ in maxs: print("   maximal:", [fmt(atoms[k], V) for k in range(len(atoms)) if s_ >> k & 1])
    valid_min = []
    for size in range(1, maxsize + 1):
        for combo in itertools.combinations(range(len(atoms)), size):
            H = sum(1 << k for k in combo)
            if any((H & s) == H for s in maxs): continue
            if any((h & H) == h for h in valid_min): continue
            if not any((H & s) == H for s in pos): continue   # vacuous: no closed instance satisfies H
            valid_min.append(H)
            if verbose: print("  ", size, [fmt(atoms[k], V) for k in combo], flush=True)
    return atoms, valid_min

def fmt(at, V):
    k = at[0]
    if k == 'comm': return f"x{V[at[1]]}={V[at[1]]}x"
    if k == 'xle': return f"x<={V[at[1]]}"
    if k == 'lex': return f"{V[at[1]]}<=x"
    if k == 'sees': return f"th_x({V[at[1]]})=th_x({V[at[2]]})"
    if k == 'seen': return f"th_{V[at[1]]}(x)=th_{V[at[2]]}(x)"
    if k == 'xeq': return f"x=th_{V[at[1]]}({V[at[2]]})"

if __name__ == "__main__":
    m = int(sys.argv[1]); n = int(sys.argv[2]); maxsize = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    run(m, n, maxsize)
