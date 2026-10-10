"""All 14-element 'octagon' projection algebras.
Elements: A1..A4, B1..B4, W, Z, M1..M4.  Operation x*y = y x y (= x theta_y).
Everything is forced by the octagon hypotheses + axioms except the antipodal values
A_i * B_{i+2} in {B_{i+2}, Z, M_{i+2}} and B_{i+2} * A_i in {A_i, W, M_i}.
We enumerate the 3^8 choices, keep those satisfying (P1)'-(P5)', and test the
hexagon condition in each."""
import itertools, re
from termeval import make_eval

names = [f"A{i}" for i in range(1, 5)] + [f"B{i}" for i in range(1, 5)] + ["W", "Z"] + [f"M{i}" for i in range(1, 5)]
idx = {s: i for i, s in enumerate(names)}
A = [idx[f"A{i}"] for i in range(1, 5)]; B = [idx[f"B{i}"] for i in range(1, 5)]
W, Z = idx["W"], idx["Z"]; M = [idx[f"M{i}"] for i in range(1, 5)]
Y = {W, Z, *M}
N = len(names)

def fA(i, y):   # f_{a_i}(y) = a_i y a_i for y in Y
    if y == W: return W
    if y == Z: return M[i]
    return M[i] if y == M[i] else W
def fB(i, y):
    if y == Z: return Z
    if y == W: return M[i]
    return M[i] if y == M[i] else Z

def base_table():
    T = [[None] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if y in Y:
                T[x][y] = y
            elif x in Y:
                T[x][y] = fA(A.index(y), x) if y in A else fB(B.index(y), x)
            elif x == y:
                T[x][y] = x
            elif x in A and y in A:
                T[x][y] = W
            elif x in B and y in B:
                T[x][y] = Z
            else:
                i = A.index(x) if x in A else A.index(y)
                j = B.index(y) if y in B else B.index(x)
                if i == j:
                    T[x][y] = M[i]
                elif (i - j) % 4 in (1, 3):          # matched: y x y = y
                    T[x][y] = y
                else:
                    T[x][y] = None                   # antipodal: free
    return T

free = [(A[i], B[(i + 2) % 4]) for i in range(4)] + [(B[(i + 2) % 4], A[i]) for i in range(4)]
choices = []
for x, y in free:
    if y in B:  # A_i * B_j: below B_j
        choices.append([y, Z, M[B.index(y)]])
    else:       # B_j * A_i: below A_i
        choices.append([y, W, M[A.index(y)]])

axioms = ["x * x = x", "(y * x) * x = y * x", "(x * y) * x = y * x",
          "((z * x) * y) * x = z * (y * x)", "(((z * x) * y) * x) * y = (z * x) * y"]
parsed = []
for a in axioms:
    l, r = a.split("="); vs = sorted(set(re.findall(r"[xyz]", a))); parsed.append((l, r, vs))

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

def hex_counterexamples(T):
    op = lambda x, y: T[x][y]; ev = make_eval(op)
    hyps = [(l, r) for l, r, neg in hexlits if neg]; concl = [(l, r) for l, r, neg in hexlits if not neg]
    vars_ = ["x1", "x2", "x3", "y1", "y2", "y3"]
    stage = [[] for _ in vars_]
    for l, r in hyps:
        vs = set(re.findall(r"[xy]\d", l + " " + r)); stage[max(vars_.index(v) for v in vs)].append((l, r))
    out = []
    def rec(k, env):
        if k == 6:
            if all(ev(l, env) != ev(r, env) for l, r in concl): out.append(dict(env))
            return
        for p in range(N):
            if p in env.values(): continue
            env[vars_[k]] = p
            if all(ev(l, env) == ev(r, env) for l, r in stage[k]): rec(k + 1, env)
        del env[vars_[k]]
    rec(0, {})
    return out

good = []
for combo in itertools.product(*choices):
    T = base_table()
    for (x, y), v in zip(free, combo):
        T[x][y] = v
    op = lambda x, y: T[x][y]; ev = make_eval(op)
    ok = True
    for l, r, vs in parsed:
        for vals in itertools.product(range(N), repeat=len(vs)):
            env = dict(zip(vs, vals))
            if ev(l, env) != ev(r, env):
                ok = False; break
        if not ok: break
    if ok:
        good.append((combo, T))
print(f"{len(good)} of {3**8} choices give projection algebras")
for combo, T in good:
    desc = ", ".join(f"{names[x]}*{names[y]}={names[v]}" for (x, y), v in zip(free, combo))
    ce = hex_counterexamples(T)
    print(f"  {desc}\n     hexagon counterexamples: {len(ce)}", end="")
    if ce:
        e = ce[0]; print("  e.g.", {v: names[e[v]] for v in sorted(e)}, end="")
    print()
