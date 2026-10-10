"""Octagon-but-no-hexagon search via *-subsemigroups of P_6 (memory-light version)."""
import sys, time, itertools, pickle, re
from pmon import projections, canon, mul as rawmul, star as pstar
from termeval import make_eval

n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
projs = projections(n); pi = {p: i for i, p in enumerate(projs)}; M = len(projs)
t0 = time.time()
comm = [set() for _ in range(M)]; mat = [set() for _ in range(M)]
for i in range(M):
    for j in range(i + 1, M):
        pq = rawmul(projs[i], projs[j], n); qp = rawmul(projs[j], projs[i], n)
        if pq == qp:
            comm[i].add(j); comm[j].add(i)
        elif rawmul(pq, projs[i], n) == projs[i] and rawmul(qp, projs[j], n) == projs[j]:
            mat[i].add(j); mat[j].add(i)
print(f"P_{n}: {M} projections, relations computed ({time.time()-t0:.0f}s)", flush=True)
def act(perm, p):
    return canon([[perm[x] if x < n else n + perm[x - n] for x in blk] for blk in p])
perms = list(itertools.permutations(range(n)))
seen = set(); reps = []
for i, p in enumerate(projs):
    if i in seen: continue
    reps.append(i)
    for perm in perms: seen.add(pi[act(perm, p)])

def general(i, j):
    return i != j and j not in mat[i] and j not in comm[i]

def candidates():
    for a1 in reps:
        for b2 in mat[a1]:
            for b4 in mat[a1] & comm[b2]:
                for a3 in mat[b2] & mat[b4] & comm[a1]:
                    for a2 in comm[a1] & comm[a3] & comm[b2]:
                        if not general(a2, b4): continue
                        for b1 in mat[a2] & comm[b2] & comm[b4]:
                            if not general(a3, b1): continue
                            for b3 in mat[a2] & comm[b1] & comm[b2] & comm[b4]:
                                if not general(a1, b3): continue
                                for a4 in mat[b1] & mat[b3] & comm[a1] & comm[a2] & comm[a3] & comm[b4]:
                                    if not general(a4, b2): continue
                                    yield (a1, a2, a3, a4, b1, b2, b3, b4)

class Mul:
    def __init__(self): self.c = {}
    def __call__(self, x, y):
        k = (x, y); r = self.c.get(k)
        if r is None:
            r = rawmul(x, y, n); self.c[k] = r
        return r

def generate(gens, mulf, cap):
    S = list(dict.fromkeys(gens)); idx = {x: i for i, x in enumerate(S)}
    frontier = list(S)
    while frontier:
        new = []
        for x in frontier:
            for y in list(S):
                for z in (mulf(x, y), mulf(y, x)):
                    if z not in idx:
                        idx[z] = len(S); S.append(z); new.append(z)
                        if len(S) > cap: return None, None
        frontier = new
    return S, idx

class UF:
    def __init__(self, k): self.p = list(range(k))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: return False
        self.p[a] = b; return True

HEX = """x1 * x2 != x2 * x3 | x1 * x2 != x3 * x1 |
y1 * y2 != y2 * y3 | y1 * y2 != y3 * y1 |
x1 * y1 != y1 * x1 | x2 * y2 != y2 * x2 | x3 * y3 != y3 * x3 |
y2 * x1 != x1 | x1 * y2 != y2 | y3 * x1 != x1 | x1 * y3 != y3 |
y1 * x2 != x2 | x2 * y1 != y1 | y3 * x2 != x2 | x2 * y3 != y3 |
y1 * x3 != x3 | x3 * y1 != y1 | y2 * x3 != x3 | x3 * y2 != y2 |
x1 * x2 = y1 * y2."""
hexlits = []
for lit in HEX.strip().rstrip(".").split("|"):
    lit = lit.strip()
    if "!=" in lit: l, r = lit.split("!="); hexlits.append((l.strip(), r.strip(), True))
    else: l, r = lit.split("="); hexlits.append((l.strip(), r.strip(), False))

def search_clause(lits, dom, op):
    ev = make_eval(op)
    vars_ = sorted({v for l, r, _ in lits for v in re.findall(r"[xy]\d", l + " " + r)})
    hyps = [(l, r) for l, r, neg in lits if neg]; concl = [(l, r) for l, r, neg in lits if not neg]
    stage = [[] for _ in vars_]
    for l, r in hyps:
        vs = set(re.findall(r"[xy]\d", l + " " + r)); stage[max(vars_.index(v) for v in vs)].append((l, r))
    out = []
    def rec(k, env):
        if out: return
        if k == len(vars_):
            if all(ev(l, env) != ev(r, env) for l, r in concl): out.append(dict(env))
            return
        for p in dom:
            if p in env.values(): continue
            env[vars_[k]] = p
            if all(ev(l, env) == ev(r, env) for l, r in stage[k]): rec(k + 1, env)
        del env[vars_[k]]
    rec(0, {})
    return out

t0 = time.time(); ncand = 0; nbig = 0; ntested = 0
for cand in candidates():
    ncand += 1
    if ncand % 500 == 0:
        print(f"  ... {ncand} candidates ({nbig} too big, {ntested} tested), {time.time()-t0:.0f}s", flush=True)
    mulf = Mul()
    gens = [projs[i] for i in cand]
    if mulf(gens[0], gens[1]) == mulf(gens[4], gens[5]): continue
    S, idx = generate(gens, mulf, CAP)
    if S is None:
        nbig += 1; continue
    k = len(S)
    T = [[idx[mulf(x, y)] for y in S] for x in S]
    st = [idx[pstar(x, n)] for x in S]
    A = [idx[projs[i]] for i in cand[:4]]; B = [idx[projs[i]] for i in cand[4:]]
    prods_a = [T[A[i]][A[j]] for i in range(4) for j in range(4) if i != j]
    prods_b = [T[B[i]][B[j]] for i in range(4) for j in range(4) if i != j]
    pairs = [(prods_a[0], x) for x in prods_a[1:]] + [(prods_b[0], x) for x in prods_b[1:]]
    uf = UF(k); todo = list(pairs)
    while todo:
        a, b = todo.pop()
        if not uf.union(a, b): continue
        todo.append((st[a], st[b]))
        for c in range(k):
            todo.append((T[a][c], T[b][c])); todo.append((T[c][a], T[c][b]))
    ntested += 1
    w, z = uf.find(prods_a[0]), uf.find(prods_b[0])
    if w == z:
        continue
    cl = {}
    for x in range(k): cl.setdefault(uf.find(x), x)
    classes = sorted(cl); qi = {c: i for i, c in enumerate(classes)}; nq = len(classes)
    Tq = [[qi[uf.find(T[cl[c]][cl[d]])] for d in classes] for c in classes]
    sq = [qi[uf.find(st[cl[c]])] for c in classes]
    projq = [x for x in range(nq) if sq[x] == x and Tq[x][x] == x]
    op = lambda x, y, Tq=Tq: Tq[Tq[y][x]][y]
    ce = search_clause(hexlits, projq, op)
    print(f"cand #{ncand}: |S|={k}, |S/rho|={nq}, {len(projq)} projections, w!=z, hexagon counterexample: {'yes' if ce else 'NO'}  ({time.time()-t0:.0f}s)", flush=True)
    if not ce:
        print("   *** SEPARATING EXAMPLE ***", [projs[i] for i in cand], flush=True)
        pickle.dump((cand, S, [uf.find(x) for x in range(k)]), open(f"octsep_{n}.pkl", "wb"))
        break
print(f"{ncand} candidates examined, {nbig} too big, {ntested} tested ({time.time()-t0:.0f}s)")
