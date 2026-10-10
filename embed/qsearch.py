"""Custom embedding search for Q = P_3/mu_1 into P_n, using generators S_3, a_0, b_0."""
import sys, time, itertools, pickle
from pmon import Pn, projections, rank, canon
from congr import quotient
from pmon import partition_monoid, mul, star as pstar

# build Q
n3 = 3
elems3 = partition_monoid(n3); idx3 = {e: i for i, e in enumerate(elems3)}
T3 = [[idx3[mul(p, q, n3)] for q in elems3] for p in elems3]
st3 = [idx3[pstar(p, n3)] for p in elems3]
congs = pickle.load(open("congs_P3.pkl", "rb"))
c103 = [c for c in congs if len(set(c)) == 103][0]
Tq, sq = quotient(T3, st3, c103)
classes = sorted(set(c103)); qidx = {cl: i for i, cl in enumerate(classes)}
q_of = lambda e: qidx[c103[idx3[e]]]
# generators in Q
c_perm = canon([[0, 4], [1, 5], [2, 3]])      # 0->1->2->0 : block {i, (i+1)'}
t_perm = canon([[0, 3], [1, 5], [2, 4]])      # (1 2)
a0 = canon([[0, 3], [1, 2, 4, 5]])            # (0 | 12), both T
b0 = canon([[1, 4], [2, 5], [0], [3]])        # (1,2 T; 0 N)
gens = [q_of(c_perm), q_of(t_perm), q_of(a0), q_of(b0)]
nQ = len(Tq)

def perm_partition(perm, n):
    return canon([[i, n + perm[i]] for i in range(n)])

def try_close(P, img):
    """extend partial map Q->P_n (dict) by products; return full map or None."""
    img = dict(img); used = {}
    for x, v in img.items():
        if v in used: return None
        used[v] = x
    changed = True
    while changed:
        changed = False
        items = list(img.items())
        for a, va in items:
            sa = sq[a]
            if sa not in img:
                w = P.star(va)
                if w in used: return None
                img[sa] = w; used[w] = sa; changed = True
            for b, vb in items:
                c = Tq[a][b]; w = P.mul(va, vb)
                if c in img:
                    if img[c] != w: return None
                else:
                    if w in used: return None
                    img[c] = w; used[w] = c; changed = True
    return img


def words_upto(gen_names, L):
    ws = []
    for l in range(1, L + 1):
        ws.extend(itertools.product(gen_names, repeat=l))
    return ws

def eval_word(w, vals, mulf, starf):
    r = None
    for ch in w:
        v = vals[ch.lower()] if ch.islower() else starf(vals[ch.lower()])
        r = v if r is None else mulf(r, v)
    return r

def coincidences(gen_names, L, vals, mulf, starf):
    """partition of words (with stars) by value"""
    names = gen_names + [g.upper() for g in gen_names]
    ws = words_upto(names, L)
    val = {w: eval_word(w, vals, mulf, starf) for w in ws}
    return ws, val

def search(n, verbose=True, L=3):
    P = Pn(n); projs = projections(n)
    perms = list(itertools.permutations(range(n)))
    def compose(p, q): return tuple(p[q[i]] for i in range(n))
    def inv(p):
        r = [0]*n
        for i, v in enumerate(p): r[v] = i
        return tuple(r)
    ident = tuple(range(n))
    reps = []; seen = set()
    for C in perms:
        if C == ident or compose(C, compose(C, C)) != ident: continue
        for Tp in perms:
            if Tp == ident or compose(Tp, Tp) != ident: continue
            if compose(Tp, compose(C, Tp)) != inv(C): continue
            key = min((compose(g, compose(C, inv(g))), compose(g, compose(Tp, inv(g)))) for g in perms)
            if key in seen: continue
            seen.add(key); reps.append((C, Tp))
    if verbose: print(f"  n={n}: {len(reps)} conjugacy classes of S_3 -> S_n; {len(projs)} projections", flush=True)
    qmul = lambda x, y: Tq[x][y]; qstar = lambda x: sq[x]
    # relations in Q among generators (c,t,a) and (c,t,b) and (c,t,a,b)
    def rel_pattern(gnames, vals):
        ws, val = coincidences(gnames, L, vals, qmul, qstar)
        return ws, val
    wsA, valA = rel_pattern(['c', 't', 'a'], {'c': gens[0], 't': gens[1], 'a': gens[2]})
    wsB, valB = rel_pattern(['c', 't', 'b'], {'c': gens[0], 't': gens[1], 'b': gens[3]})
    wsAB, valAB = rel_pattern(['c', 't', 'a', 'b'], {'c': gens[0], 't': gens[1], 'a': gens[2], 'b': gens[3]})
    def ok(ws, valQ, vals):
        valP = {}
        for w in ws:
            valP[w] = eval_word(w, vals, P.mul, P.star)
        # equal in Q => equal in P; and distinct in Q => distinct in P
        rep = {}
        for w in ws:
            q = valQ[w]; p = valP[w]
            if q in rep:
                if rep[q] != p: return False
            else:
                rep[q] = p
        return len(set(rep.values())) == len(rep)
    count = 0
    for C, Tp in reps:
        Cp = perm_partition(C, n); Tpp = perm_partition(Tp, n)
        a0c = [a for a in projs if ok(wsA, valA, {'c': Cp, 't': Tpp, 'a': a})]
        b0c = [b for b in projs if ok(wsB, valB, {'c': Cp, 't': Tpp, 'b': b})]
        if verbose: print(f"    class {C},{Tp}: {len(a0c)} a0-candidates, {len(b0c)} b0-candidates", flush=True)
        for a in a0c:
            for b in b0c:
                if P.rank(b) != P.rank(a): continue
                if not ok(wsAB, valAB, {'c': Cp, 't': Tpp, 'a': a, 'b': b}): continue
                count += 1
                img = try_close(P, {gens[0]: Cp, gens[1]: Tpp, gens[2]: a, gens[3]: b})
                if img is not None and len(img) == nQ:
                    return img
    if verbose: print(f"    {count} full closure attempts, none succeeded", flush=True)
    return None

if __name__ == "__main__":
    for n in range(3, int(sys.argv[1]) + 1):
        t = time.time()
        res = search(n)
        print(f"n={n}: {'EMBEDS' if res else 'no embedding'} ({time.time()-t:.0f}s)", flush=True)
        if res:
            for g in gens: print("  ", g, "->", res[g])
            break
