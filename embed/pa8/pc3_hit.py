"""Minimal path-closing quasi-identities (two auxiliaries, chords) violated by a given projection algebra C.
For every instance in C of a matched path p_0 ~ ... ~ p_n (distinct vertices) with p_0 !~ p_n and auxiliaries x != y
not on the path, the C-signature S (atoms true in C) is computed; a hypothesis set H subset of S is valid in P(P_m) iff
H is contained in no maximal negative signature (pc3sig_m_n.pkl), i.e. H hits every set S \\ s (s maximal negative);
minimal hitting sets up to size K are enumerated (branch and bound), and kept if non-vacuous (contained in a positive
signature).  Usage: python3 pc3_hit.py m n K  cand_index|P7  [more indices]"""
import sys, os, json, pickle, itertools
EMBED = os.environ.get("EMBED_DIR", "/mnt/user-data/outputs/starsemigroup/embed"); sys.path.insert(0, EMBED)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathclose3 import fmt2

def sig_of(A, P, x, y, atoms):
    th = lambda p, q: A[q][p]
    le = lambda p, q: th(q, p) == p
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    Z = {'x': x, 'y': y}
    s = 0
    for k, at in enumerate(atoms):
        if at[0] == 'ch': v = mt(P[at[1]], P[at[2]])
        elif at[0] in ('x', 'y'):
            z, kd = Z[at[0]], at[1]
            if kd == 'comm': v = th(z, P[at[2]]) == th(P[at[2]], z)
            elif kd == 'zle': v = le(z, P[at[2]])
            elif kd == 'lez': v = le(P[at[2]], z)
            elif kd == 'sees': v = th(z, P[at[2]]) == th(z, P[at[3]])
            elif kd == 'seen': v = th(P[at[2]], z) == th(P[at[3]], z)
            elif kd == 'zeq': v = th(P[at[2]], P[at[3]]) == z
        else:
            kd = at[1]
            if kd == 'comm': v = th(x, y) == th(y, x)
            elif kd == 'xley': v = le(x, y)
            elif kd == 'ylex': v = le(y, x)
            else:
                i = P[at[2]]
                if kd == 'sees': v = th(x, i) == th(y, i)
                elif kd == 'seen': v = th(i, x) == th(i, y)
                elif kd == 'x=th_y': v = th(y, i) == x
                elif kd == 'y=th_x': v = th(x, i) == y
                elif kd == 'x=th_p_y': v = th(i, y) == x
                elif kd == 'y=th_p_x': v = th(i, x) == y
        if v: s |= 1 << k
    return s

def min_hitting(sets, K):
    """minimal hitting sets (as bitmasks) of size <= K of a family of bitmask sets; simple branch and bound"""
    sets = sorted(set(sets), key=lambda s: bin(s).count('1'))
    if any(s == 0 for s in sets): return []
    res = []
    def rec(H, size, remaining):
        if not remaining:
            res.append(H); return
        if size == K: return
        s = min(remaining, key=lambda t: bin(t).count('1'))
        bits = [b for b in range(s.bit_length()) if s >> b & 1]
        for b in bits:
            rec(H | (1 << b), size + 1, [t for t in remaining if not t >> b & 1])
    rec(0, 0, sets)
    # keep minimal ones only
    res = sorted(set(res), key=lambda h: bin(h).count('1')); out = []
    for h in res:
        if not any((g & h) == g for g in out): out.append(h)
    return out

def violated_qis(A, m, n, K, verbose=True):
    d = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"pc3sig_{m}_{n}.pkl"), "rb"))
    atoms, maxs, pos = d["atoms"], d["maxs"], d["pos"]
    N = len(A); th = lambda p, q: A[q][p]
    mt = lambda p, q: th(p, q) == p and th(q, p) == q
    matched = {p: [q for q in range(N) if q != p and mt(p, q)] for p in range(N)}
    V = ['p%d' % i for i in range(n + 1)]
    found = {}
    def paths(prefix):
        if len(prefix) == n + 1: yield prefix; return
        for q in matched[prefix[-1]]:
            if q not in prefix: yield from paths(prefix + [q])
    for p0 in range(N):
        for P in paths([p0]):
            if mt(P[0], P[-1]): continue
            for x in range(N):
                if x in P: continue
                for y in range(N):
                    if y in P or y == x: continue
                    S = sig_of(A, P, x, y, atoms)
                    fam = [S & ~s for s in maxs]
                    for H in min_hitting(fam, K):
                        if not any((H & s) == H for s in pos): continue
                        if H not in found: found[H] = (P, x, y)
    for H in sorted(found, key=lambda h: bin(h).count('1')):
        P, x, y = found[H]
        if verbose: print(f"  {bin(H).count('1')} {[fmt2(atoms[k], V) for k in range(len(atoms)) if H >> k & 1]}   instance P={P}, x={x}, y={y}")
    return found

if __name__ == "__main__":
    m, n, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    recs = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "post8.log"))]
    cands = [r["A"] for r in recs if r["embeds"] is None]
    from fourth import table as P7table
    for a in sys.argv[4:]:
        A = P7table() if a == "P7" else cands[int(a)]
        print(f"=== {a} ===")
        violated_qis(A, m, n, K)

def full_valid_ones(A, m, n, K, m2=5, verbose=True):
    """hitting sets that are valid without distinctness assumptions (SAT at m, then m2)"""
    from pc3_verify import valid
    import pickle
    d = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"pc3sig_{m}_{n}.pkl"), "rb"))
    atoms = d["atoms"]; V = ['p%d' % i for i in range(n + 1)]
    found = violated_qis(A, m, n, K, verbose=False)
    good = []
    for H in sorted(found, key=lambda h: bin(h).count('1')):
        Hl = [atoms[k] for k in range(len(atoms)) if H >> k & 1]
        if any((g & H) == g for g in good): continue          # superset of an already verified set
        if not valid(Hl, n, m): continue
        ok2 = valid(Hl, n, m2) if m2 else True
        if ok2: good.append(H)
        P, x, y = found[H]
        if verbose: print(f"  {len(Hl)} {('VALID(%d)' % m2) if (ok2 and m2) else ('valid(%d)' % m)} {[fmt2(a, V) for a in Hl]}   instance P={P}, x={x}, y={y}", flush=True)
    return good
