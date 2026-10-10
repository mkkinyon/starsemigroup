"""Sanity check of hexagon.in: parse its equations and evaluate them
(a) the axioms (P1)'-(P5)' on the projection algebras of P_2, P_3, P_4 and of Q = P_3/mu,
(b) the hexagon hypotheses on Q with the intended assignment, checking w != z.
Binary operation:  x * y := y x y  (semigroup product), i.e.  x * y = x theta_y."""
import re, itertools, pickle
from pmon import Pn, projections, partition_monoid, mul, star as pstar, canon
from congr import quotient

# ---- parse hexagon.in ----
src = open("hexagon.in").read()
src = re.sub(r"%.*", "", src)
assum = src.split("formulas(assumptions).")[1].split("end_of_list.")[0]
eqs = [e.strip() for e in assum.split(".") if e.strip()]
axioms = [e for e in eqs if re.fullmatch(r"[xyz()* =]+", e)]
hyps = [e for e in eqs if e not in axioms]
print(len(axioms), "axioms;", len(hyps), "hypothesis equations")

def make_eval(op):
    def ev(term, env):
        term = term.strip()
        # strip outer parentheses
        while term.startswith("(") and term.endswith(")"):
            depth = 0; ok = True
            for i, ch in enumerate(term):
                depth += ch == "("; depth -= ch == ")"
                if depth == 0 and i < len(term) - 1:
                    ok = False; break
            if ok: term = term[1:-1].strip()
            else: break
        # split at top-level '*'
        depth = 0
        for i, ch in enumerate(term):
            depth += ch == "("; depth -= ch == ")"
            if depth == 0 and ch == "*":
                return op(ev(term[:i], env), ev(term[i+1:], env))
        return env[term]
    return ev

def check_axioms(P, projs):
    op = lambda x, y: P.prod(y, x, y)
    ev = make_eval(op)
    for ax in axioms:
        lhs, rhs = ax.split("=")
        vars_ = sorted(set(re.findall(r"[xyz]", ax)))
        for vals in itertools.product(projs, repeat=len(vars_)):
            env = dict(zip(vars_, vals))
            if ev(lhs, env) != ev(rhs, env):
                return ax
    return None

for n in (2, 3, 4):
    P = Pn(n); projs = projections(n)
    print(f"P_{n}: axioms", "OK" if check_axioms(P, projs) is None else "FAIL")

# ---- Q = P_3/mu ----
n3 = 3
elems3 = partition_monoid(n3); idx3 = {e: i for i, e in enumerate(elems3)}
T3 = [[idx3[mul(p, q, n3)] for q in elems3] for p in elems3]
st3 = [idx3[pstar(p, n3)] for p in elems3]
congs = pickle.load(open("congs_P3.pkl", "rb"))
c103 = [c for c in congs if len(set(c)) == 103][0]
Tq, sq = quotient(T3, st3, c103)
classes = sorted(set(c103)); qidx = {cl: i for i, cl in enumerate(classes)}
q_of = lambda e: qidx[c103[idx3[e]]]
class QS:
    def prod(self, *xs):
        r = xs[0]
        for y in xs[1:]: r = Tq[r][y]
        return r
Q = QS()
projQ = [x for x in range(len(Tq)) if sq[x] == x and Tq[x][x] == x]
print(f"Q = P_3/mu: {len(Tq)} elements, {len(projQ)} projections; axioms",
      "OK" if check_axioms(Q, projQ) is None else "FAIL")

# intended assignment (points 0,1,2; i <-> i-1)
def a(i):  # T-blocks {i}, complement
    others = [j for j in range(3) if j != i]
    return canon([[i, 3 + i], others + [3 + j for j in others]])
def b(i):  # T-blocks the two singletons != i, N-blocks {i},{i'}
    others = [j for j in range(3) if j != i]
    return canon([[j, 3 + j] for j in others] + [[i], [3 + i]])
env = {}
for i in range(3):
    env[f"a{i+1}"] = q_of(a(i)); env[f"b{i+1}"] = q_of(b(i))
op = lambda x, y: Q.prod(y, x, y)
ev = make_eval(op)
env["cw"] = op(env["a1"], env["a2"]); env["cz"] = op(env["b1"], env["b2"])
for i in range(3):
    env[f"m{i+1}"] = op(env[f"a{i+1}"], env[f"b{i+1}"])
bad = [h for h in hyps if ev(*h.split("=")[:1], env) != ev(h.split("=")[1], env)]
print("hypotheses failing in Q:", bad)
print("w == z in Q ?", env["cw"] == env["cz"])
print("w, z, m_i distinct:", len({env[k] for k in ("cw", "cz", "m1", "m2", "m3")}))
# the same six projections in P_3 itself: which hypotheses fail there?
P3 = Pn(3); op3 = lambda x, y: P3.prod(y, x, y); ev3 = make_eval(op3)
env3 = {f"a{i+1}": a(i) for i in range(3)}; env3.update({f"b{i+1}": b(i) for i in range(3)})
env3["cw"] = op3(env3["a1"], env3["a2"]); env3["cz"] = op3(env3["b1"], env3["b2"])
for i in range(3):
    env3[f"m{i+1}"] = op3(env3[f"a{i+1}"], env3[f"b{i+1}"])
bad3 = [h for h in hyps if ev3(h.split("=")[0], env3) != ev3(h.split("=")[1], env3)]
print("hypotheses failing in P_3 itself:", bad3)
